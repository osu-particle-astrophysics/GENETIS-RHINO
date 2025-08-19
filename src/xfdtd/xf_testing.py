"""File to run XFdtd simulation tests to make sure files work."""

# File paths relevant to PUEO are left in comments next to where they have been altered for reference

from pathlib import Path
import subprocess
import logging
import shutil
import time

log = logging.getLogger(__name__)

# Unsure how to handle the lack of a settings file so here's a big dictionary for now
settings = {"npop": 5, "a_type": "VPOL", "curved": 0, "sep": 0, "nsections": 0}  # These are all the settings["string"] references that exist in this script, if a necessary parameter is missing for testing...
                                                                                 # then there is a deeper issue afoot

# Put temporary genes for testing
S = 43.56390557099357;    # Side length of bottom of antenna
H = 92.1400468575904;    # Height of antenna
X0 = 21.486696410391534;    # distance from center of ridges at bottom // previously 0.04
Y0 = 15.048860479719881;    # (half) width of ridges at bottom // previously 0.04
Z0 = 10.9332;    # initial height of ridges (0 always for now)
Xf = 15.2005;    # final distance from center of curve of ridges at max height
Yf = 2.2304128114770774;    # final width of ridges at max height
Zf = 33.36388836919369;    # max height of ridges
Beta = 0.126047394660302;    # curvature of ridges
L = 0.8262871305406002;    # (half) width of minor length of trapezoid extrude
h = 9.776272366906996;    # "height" of trapezoid extrude (in x-y plane; must be < x0)

# Class from the PUEO script that is probably necessary in my (Byron's) view, but I am not super familiar with this scripting
class XFRunner:
    def __init__(self, run_dir: Path, run_name: str, gen: int, settings: dict):
        self.run_dir = Path(run_dir)
        self.run_name = run_name
        self.gen = gen
        self.settings = settings

        self.workingdir = Path("GENETIS-RHINO" / "src" / "xfdtd")   # Path(settings["workingdir"])
        self.npop = settings["npop"]
        self.xf_proj = Path("GENETIS-RHINO" / "src" / "xfdtd")       #settings["xf_proj"]
        self.xmacros_dir = Path("GENETIS-RHINO" / "src" / "xfdtd")   # settings["xmacros"]
        self.run_xmacros_dir = Path("GENETIS-RHINO" / "src" / "xfdtd") ## <- The directory that all of XF Team's work exists in #Path(settings["run_xmacros"])
        self.a_type = settings["a_type"]

        self.csv_dir = self.run_dir / "Generation_Data" / str(self.gen) / "csv_files"
        self.csv_dir.mkdir(parents=True, exist_ok=True, mode=0o775)

# Function for setting up simulation setup + building scripts
  def _create_simulation_macro_vpol(self):
          macro_path = self.run_xmacros_dir / "BuildingScripts.js" #self.run_xmacros_dir / "simulation_PEC.xmacro"
          with macro_path.open("w") as f:
              f.write(f"var NPOP = {self.npop};\n")
              f.write("var indiv = 1;\n")
              f.write(f"var gen = {self.gen};\n")
              f.write(f'var workingdir = "{self.workingdir}";\n')
              f.write(f'var RunName = "{self.run_name}";\n')
              f.write(f"var freq_start = {self.settings['freq_start']};\n")
              f.write(f"var freq_step = {self.settings['freq_step']};\n")
              f.write(f"var freqCoefficients = {self.settings['freq_num']};\n")
              f.write(f"var CURVED = {self.settings['curved']};\n")
              f.write(f"var NSECTIONS = {self.settings['nsections']};\n")
              f.write(f"var evolve_sep = {self.settings['sep']};\n")
              if self.gen == 0:
                  f.write(
                      f'App.saveCurrentProjectAs("{self.run_dir / self.run_name}");\n'
                  )

             # move this inside the same with block so f stays open
              vpol_macro_parts = [
                  "header_vpol.js",
                  "calls_vpol.js",
                  "build_vpol.js",
                  "vpol_feed.js",
                  "create_grid_vpol.js",
              ]
              shared_macro_parts = [
                  "create_pec.js",
                  "create_sensors.js",
                  "create_ant_sim_data.js",
                  "queue_sim.js",
                  "make_image.js",
              ]
              for part in vpol_macro_parts:
                 with open(self.xmacros_dir / part) as src:  # Unsure where the RHINO equivalent of "part" would be
                      f.write(src.read())
              for part in shared_macro_parts:
                 with open(self.xmacros_dir / part) as src:
                      f.write(src.read())
           macro_path.chmod(0o775)

           log.info(f"simulation_PEC.xmacro created at {macro_path}")

  def _run_build_macro(self):  
        macro_path = self.run_xmacros_dir / "BuildingScripts.js" #self.run_xmacros_dir / "simulation_PEC.xmacro"
        cmd = ["xfdtd", str(self.xf_proj), f"--execute-macro-script={macro_path}"]
        try:
            subprocess.run(cmd, check=True)
            log.info("XF building macro executed.")
        except subprocess.CalledProcessError as e:
            log.warning("XF macro building execution failed or was interrupted.")
            log.warning(e)
        
# Function to submit xf simulation job
    def _submit_jobs(self):
        num_keys = self.settings["num_keys"]
        batch_size = min(self.npop, num_keys)
        job_time = "04:00:00"
        subprocess.run(["scancel", "-n", self.run_name], check=False)
        cmd = [
            "sbatch",
            f"--array=1-{self.npop}%{batch_size}",
            f"--export=ALL,WorkingDir={self.workingdir},RunName={self.run_name},"
            f"indiv=0,gen={self.gen},batch_size={batch_size},NPOP={self.npop},"
            f"XFProj={self.xf_proj}",
            f"--job-name={self.run_name}",
            f"--time={job_time}",
            str(self.workingdir / "xf_gpu.sh"),  # self.workingdir / "src" / "xf" / "shared_scripts" / "xf_gpu.sh"
        ]
        subprocess.run(cmd, check=True)
        log.info(f"Submitted XF jobs with batch size {batch_size}.")

# Function to output xf files (uan and s11)
    def _create_output_macro(self):
        macro_path = self.run_xmacros_dir / "shortened_outputmacroskeleton.js" ### NOT YET IN DIRECTORY and will probably be renamed. # self.run_xmacros_dir / "output.xmacro"
        with macro_path.open("w") as f:
            f.write(f"var popsize = {self.npop};\n")
            f.write(f"var gen = {self.gen};\n")
            f.write(f'var workingdir = "{self.workingdir}";\n')
            f.write(f'var RunDir = "{self.run_dir}";\n')
            with open(self.xmacros_dir / "shortened_outputmacroskeleton.js" ) as src: # Either this or the above "macro_path" variable is the wrong place to have this .js file I believe # open(self.xmacros_dir / "shared_scripts" / "output_skele.js")
                f.write(src.read())
        macro_path.chmod(0o775)
        log.info(f"output.xmacro created at {macro_path}")

    def _run_output_macro(self):
        macro_path = self.run_xmacros_dir / "shortened_outputmacroskeleton.js" ### NOT YET IN DIRECTORY and will probably be renamed. #"output.xmacro"
        cmd = ["xfdtd", str(self.xf_proj), f"--execute-macro-script={macro_path}"]
        try:
            subprocess.run(cmd, check=True)
            log.info("XF output macro executed.")
        except subprocess.CalledProcessError as e:
            log.warning("XF output macro execution failed or was interrupted.")
            log.warning(e)
