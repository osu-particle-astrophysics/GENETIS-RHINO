"""xf_job.py contains class pertaining to running an individual through XFdtd to get antenna performance. Using persistent XF instance in VDI."""

import asyncio
import getpass
import json
import shutil
import subprocess
import time
from pathlib import Path

import numpy as np
import psutil

from src.GENETIS_RHINO.parameters import ParametersObject
from src.GENETIS_RHINO.genotype import Genotype

# TODO: If there is a way to automatically submit a VDI that would be awesome. You'd still need one to start a run since you have to press no on XFdtd
# TODO: Adjust convergence settings to be less rigourous in precision

# TODO: Debug


class XFdtdSim:
    """
    Class that puts individual through XFdtd antenna simulation.

    Reads in individual's genes, simulates in XFdtd, outputs simulation data.
    Outputs uan files which contain gain + phase data in all directions and VSWR, S11, + Impedance data in a csv.
    XFdtd scripts (xmacros) are in a weird version of QTScript, which is based on Javascript
    and are stored in separate javascript files in scripts directory.
    Bash script to run XFdtd antenna simulation is also in scripts folder.
    """

    _xf_lock = asyncio.Lock()

    def __init__(self, run_dir: Path, cfg: ParametersObject):
        # Directories
        self.cfg = cfg
        self.run_dir = run_dir
        self.xfproj = Path(f"{self.run_dir}/{run_dir.name}.xf")
        self.xf_scripts = Path(__file__).parent / "scripts"
        self.xf_run_scripts = self.run_dir / "xf_scripts"

        # Frequencies
        self.freqs = np.arange(
            cfg.freq_start, cfg.freq_end + cfg.freq_step, cfg.freq_step
        )
        self.num_freqs = len(self.freqs)

        # Paths for Persistent XF files
        if not Path.exists(self.xf_run_scripts):
            Path.mkdir(self.xf_run_scripts, parents=True)
        if not Path.exists(self.xf_run_scripts / "setup"):
            Path.mkdir(self.xf_run_scripts / "setup", parents=True)
        if not Path.exists(self.xf_run_scripts / "output"):
            Path.mkdir(self.xf_run_scripts / "output", parents=True)

    async def antenna_sim(self, indv_id: int, indv_genes: Genotype) -> None:
        """
        Setup and run XFdtd simulation to allow for antenna indv.
        Individual to indvuate is given in class declaration.

        Args:
            indv_id (int): Individual number
            indv_genes (Genotype): Genetic information for current indv

        Returns:
            indv_uan_dir (Path): Path to individuals uan file(s)

        """
        # Create indv_dir for this individual
        indv_dir = self.setup_indv(indv_id)

        # Check if XF GUI instance is open, if not open one
        await self.persistent_xf()

        # Parse genes to be in json format
        json_str = await self.to_xf_readable(indv_genes)

        # Create setup json file for XF instance to read in then setup simulation and antenna
        self.sim_setup(indv_id, indv_dir, json_str)

        # Submit and wait for a simulation job for antenna performance
        await self.sim_job(indv_id)

        # Output data files for XFdtd for analysis
        self.sim_output(indv_id, indv_dir)

        return indv_dir / "uan_files"

    def setup_indv(self, indv_id: int) -> Path:
        """
        Creates and sets up individuals directory where data will be stored.

        Args:
            indv_id (int): individual id

        Returns:
            indv_dir

        """
        # TODO: Is this where individual data should be stored?
        indv_dir = self.run_dir / str(indv_id)
        uan_dir = indv_dir / "uan_files"

        if not Path.exists(indv_dir):
            Path.mkdir(indv_dir, parents=True)
        if not Path.exists(uan_dir):
            Path.mkdir(uan_dir, parents=True)

        return indv_dir

    def run_xfdtd(self, persistent_dir: Path) -> None:
        """
        Opens XFdtd with script that continually checks script directory for indviduals to run.

        Args:
            persistent_dir (Path): Path to location of persistent file stored per run

        """
        persistent_xmacro = persistent_dir / "persistent_XF.xmacro"
        project_path = Path(self.run_dir) / f"{self.run_dir.name}.xf"

        js_files = [
            "xf_persistent.js",
            "xf_sim_settings.js",
            "xf_geometry.js",
            "xf_feed.js",
            "xf_output.js",
        ]
        with open(persistent_xmacro, "w") as f:
            if not project_path.exists():
                f.write(
                    f'App.saveCurrentProjectAs("{self.run_dir}/{self.run_dir.name}.xf");\n'
                )
            f.write(f'var xf_run_scripts = "{self.xf_run_scripts}";\n')
            for js in js_files:
                js_path = self.xf_scripts / js
                if Path.is_file(js_path):
                    with open(js_path) as jsf:
                        js_str = jsf.read()
                        f.write(js_str)
                        f.write("\n")
                else:
                    print(f"Warning: {js_path} not found and skipped.")
                    return
            f.write("App.quit();\n")

        xfdtd_path = shutil.which("xfdtd")
        subprocess.Popen(
            [
                xfdtd_path,
                str(self.xfproj),
                f"--execute-macro-script={persistent_xmacro}",
            ]
        )

    async def to_xf_readable(self, indv_genes: Genotype) -> None:
        """
        Convert genes to json format to allow for XFdtd input.

        Args:
            indv_genes (Genotype): indv genes

        Returns:
            json_str (str): json formatted dictionary entry of genes needed for XF to build an individual

        """
        indv_dict = {}
        indv_dict["flare_length"] = indv_genes.flare_length
        indv_dict["waveguide_height"] = indv_genes.waveguide_height
        indv_dict["waveguide_length"] = indv_genes.waveguide_length
        indv_dict["waveguide_width"] = indv_genes.waveguide_width
        for i, wall_pair in enumerate(indv_genes.walls):
            walls = {}
            walls["number"] = i
            walls["angle"] = wall_pair.angle
            walls["ridge_height"] = wall_pair.ridge_height
            walls["ridge_width_top"] = wall_pair.ridge_width_top
            walls["ridge_width_bottom"] = wall_pair.ridge_width_bottom
            walls["ridge_thickness_top"] = wall_pair.ridge_thickness_top
            walls["ridge_thickness_bottom"] = wall_pair.ridge_thickness_bottom
            indv_dict[f"wall_pair{i}"] = walls

        json_str = json.dumps(
            indv_dict, cls=NpEncoder, separators=(", ", ": "), indent=1
        )

        return json_str

    def sim_setup(self, indv_id: int, indv_dir: Path, json_str: str) -> any:
        """
        Create file to build individual and setup simulation in XFdtd before simulation.

        Args:
            indv (int): current indv
            indv_dir (Path): directory for current indv
            json_str (str): json string of dictionary for indv

        Returns:
            None if Paths not found.

        """
        sim_dir = self.xfproj / "Simulations" / f"{indv_id:06d}"
        if not sim_dir.exists():
            print(f"Running modelling for indv {indv_id}")
            setup_json = self.xf_run_scripts / "setup" / f"{indv_id}.json"
            setup_data = {
                "indv": indv_id,
                "num_wallpairs": self.cfg.NUM_WALL_PAIRS,  # TODO: Same for all individuals?
                "indvdata": json.loads(json_str),
                "indv_dir": str(indv_dir),
                "units": f" {self.cfg.xf_units}",
                "freqs": self.freqs.tolist(),
                "num_freqs": self.num_freqs,
                "freq_scale": f" {self.cfg.freq_scale}",
                "enable_sparams": self.cfg.enable_sparams,
            }
            with open(setup_json, "w") as f:
                f.write(json.dumps(setup_data, indent=4))

            shutil.copy2(setup_json, indv_dir / f"{indv_id}.json")

            setup_done = sim_dir / "status.dat"
            while True:
                if setup_done.exists():
                    with open(setup_done) as f:
                        content = f.read()
                    if "Created" in content:
                        print(f"Simulation created for individual {indv_id}.")
                        # Makes images go away????
                        setup_json.unlink()
                        break

    async def sim_job(self, indv: int) -> None:
        """
        Submits and waits for XFdtd antenna simulation job to complete.

        Args:
            indv (int): current indv

        """
        sim_status = self._get_status_file(indv)
        job_name = self.run_dir.name + str(indv)
        if sim_status.exists():
            print(f"Evaluation {indv} is complete!")
            return

        running = await self._is_job_running(self.run_dir.name + str(indv))
        if running:
            print(f"Evaluation {indv} is currently running!")
            await self._wait_for_completion(job_name, sim_status)
            return

        print(f"Submitting XF job for indv {indv}!")
        await self._submit_job(indv)
        await self._wait_for_completion(job_name, sim_status)

    def sim_output(self, indv_id: int, indv_dir: Path) -> None:
        """
        Outputs Antenna simulation data from XF simulation data.

        Args:
            indv_id (int): Current indv
            indv_dir (Path): Path to directory for indv for output.

        Raises:
            ValueError if output files are not able to be created.

        """
        uan_dir = indv_dir / "uan_files"
        uan_dir.mkdir(parents=True, exist_ok=True)

        out_json = self.xf_run_scripts / "output" / f"{indv_id}.json"
        out_data = {
            "indv_dir": str(indv_dir),
            "indv_num": indv_id,
            "num_freqs": self.num_freqs,
        }
        with open(out_json, "w") as f:
            json.dump(out_data, f, indent=4)

        while True:
            num_files = len([f for f in uan_dir.iterdir() if f.is_file()])

            if num_files >= self.num_freqs:
                print(f"Found {num_files} files for individual {indv_id}.")
                out_json.unlink()
                break

        # NOTE: We have outputs, removing the simulation data to save space
        # Without this XF projects get large, quickly with data that we don't need for evolution
        sim_dir = self.xfproj / "Simulations" / f"{indv_id:06d}"
        # Try to robustly rmtree with retries
        retries = 10
        delay = 0.5
        for attempt in range(retries):
            try:
                shutil.rmtree(sim_dir)
                break
            except OSError as e:
                if attempt < retries - 1:
                    time.sleep(delay * (attempt + 1))
                else:
                    raise OSError("Failed to sim delete") from e

    def _get_status_file(self, indv: int) -> Path:
        """Returns path to xfdtd status file."""
        return (
            self.xfproj
            / "Simulations"
            / f"{indv:06d}"
            / "Run0001"
            / "output"
            / "status"
            / "runstatus.complete"
        )

    async def _is_job_running(self, job_name: str) -> bool:
        """Check if a job with this name is running in SLURM."""
        proc = await asyncio.create_subprocess_exec(
            "squeue",
            "--name",
            job_name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        return len(stdout.decode().strip().splitlines()) > 1

    async def _wait_for_completion(self, job_name: str, status_file: Path) -> None:
        """Wait until job disappears from queue and status file appears."""
        while True:
            running = await self._is_job_running(job_name)
            if not running and status_file.exists():
                print(f"[Job] Job {job_name} completed successfully.")
                return

    async def _submit_job(self, indv: int) -> None:
        """Submit a SLURM job for this simulation."""
        submit_script = self.xf_scripts / "xfdtd_sim.sh"
        job_name = self.run_dir.name + str(indv)

        sim_dir = self.xfproj / "Simulations" / f"{indv:06d}"
        job_out_dir = self.run_dir / "slurm_logs"
        job_out_dir.mkdir(parents=True, exist_ok=True)

        output_file = job_out_dir / f"XFdtd_{job_name}.out"
        error_file = job_out_dir / f"XFdtd_{job_name}.err"

        cmd = [
            "sbatch",
            f"--job-name={job_name}",
            f"--output={output_file}",
            f"--error={error_file}",
            f"--export=ALL,sim_dir={sim_dir},joboutdir={job_out_dir}",
            str(submit_script),
        ]

        await asyncio.to_thread(subprocess.run, cmd, check=True)

    async def persistent_xf(self):
        """
        Ensures only one XF GUI instance is launched at a time.
        Respects the GUI lock without using a one-shot flag.
        """
        async with XFdtdSim._xf_lock:
            # Check if a GUI instance is already running
            if is_running("xfui_exe"):
                # Someone else started it, or it was already running
                return

            # Launch the GUI
            print("Opening Persistent XF GUI")

            self.run_xfdtd(self.run_dir)

            # Wait for the OS to register the process
            # This prevents another task from thinking GUI isn't running yet
            for _ in range(10):  # retry for ~5 seconds
                await asyncio.sleep(0.5)
                if is_running("xfui_exe"):
                    break
            else:
                print("Warning: XF GUI did not appear in OS after launch")


# Helper functions


class NpEncoder(json.JSONEncoder):
    """Helper class for json conversion."""

    def default(self, obj: any) -> str:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def is_running(process_name: str) -> bool:
    """Checks if process is running on current user."""
    current_user = getpass.getuser().lower()
    process_name = process_name.lower()

    for proc in psutil.process_iter(attrs=["name", "exe", "username"]):
        try:
            name = (proc.info["name"] or "").lower()
            exe = (proc.info["exe"] or "").lower()
            user = (proc.info["username"] or "").lower()

            if user != current_user:
                continue

            if name == process_name or exe.endswith(process_name):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return False
