"""xf_job.py contains class pertaining to running an individual through XFdtd to get antenna performance."""

import asyncio
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

import numpy as np
import psutil

## Future Tasks
# TODO: If there is a way to automatically submit a VDI that would be awesome. You'd still need one to start a run since you have to press no on XFdtd
# TODO: Adjust convergence settings to be less rigourous in precision

## Current Tasks
# TODO: Fully integrate into RHINO system
# TODO: Adjust to RHINO gene class system. This will require changing to_xf_readable function to whatever the input will be.
# TODO: Change building scripts in xf_geometry.js to be RHINO functions
# TODO: In xf_geometry.js, adjust the buildling scripts to take in genes from loop.
# Currently it has confusing variables compared to what the GA is supposed to output.
# TODO: Adjust how feed(s) are setup w/ feed script from PUEO


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

    def __init__(self, run_dir: Path, cfg: any) -> None:
        """Initialize."""
        # Directories
        self.cfg = cfg
        self.run_dir = run_dir
        self.xfproj = Path(f"{run_dir}/{cfg.run_name}.xf")
        self.xf_scripts = Path(
            f"{cfg.working_dir}/src/xfdtd/scripts",
        )  # TODO: Make sure working_dir is defined or maybe a better way.
        self.xf_run_scripts = run_dir / "xf_scripts"

        # Frequencies
        self.freqs = np.arange(cfg.freq_start, cfg.freq_end + cfg.freq_step, cfg.freq_step)
        self.num_freqs = len(self.freqs)

    async def antenna_sim(self, indv_genes: any, indv_dir: Path) -> None:
        """
        Setup and run XFdtd simulation to allow for antenna indv.

        Individual to indvuate is given in class declaration.

        Args:
            indv_genes (ShapeIndividual): Genetic information for current indv
            indv_dir (Path): Path to individuals directory

        Returns:
            Individual antenna simulation data.

        """
        await self.persistent_xf()

        indv = indv_genes.id_
        json_str = await self.to_xf_readable(indv_genes)

        self.sim_setup(indv, indv_dir, json_str)

        await self.sim_job(indv)

        self.sim_output(indv, indv_dir)

    def run_xfdtd(self, persistent_dir: Path) -> None:
        """
        Opens XFdtd with script that continually checks script directory for indviduals to run.

        Args:
            persistent_dir (Path): Path to location of persistent file stored per run

        """
        persistent_xmacro = persistent_dir / "persistent_XF.xmacro"  # TODO: Do we want this in the run directory?

        js_files = ["xf_persistent.js", "xf_sim.js", "xf_geometry.js", "xf_feed.js", "xf_output.js"]
        with open(persistent_xmacro, "w") as f:
            f.write(f'App.saveCurrentProjectAs("{self.run_dir / self.cfg.run_name}");\n')
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
        subprocess.Popen([xfdtd_path, str(self.xfproj), f"--execute-macro-script={persistent_xmacro}"])  # noqa: S603

    async def to_xf_readable(self, indv_genes: any) -> str:
        """
        Convert genes to json format to allow for XFdtd input.

        Args:
            indv_genes (ShapeIndividual): indv genes

        Returns:
            json_str (str): json formatted dictionary entry of genes needed for XF to build an individual

        """
        # TODO: Change this to pull only needed genes from indv_genes? IDK if there will be anything requiring this
        json_str = json.dumps(indv_genes, cls=NpEncoder, separators=(", ", ": "), indent=1)

        return json_str

    def sim_setup(self, indv: int, indv_dir: Path, json_str: str) -> any:
        """
        Create file to build individual and setup simulation in XFdtd before simulation.

        Args:
            indv (int): current indv
            indv_dir (Path): directory for current indv
            json_str (str): json string of dictionary for indv

        Returns:
            None if Paths not found.

        """
        sim_dir = self.xfproj / "Simulations" / f"{indv:06d}"
        if not sim_dir.exists():
            print(f"Running modelling for indv {indv}")
            setup_json = self.xf_run_scripts / "setup" / f"{indv}.json"
            setup_data = {
                "indv": indv,
                "indvdata": json.loads(json_str),
                "indv_dir": str(indv_dir),
                "units": f" {self.cfg.xf_units}",
                "ishollow": self.cfg.is_hollow,
                "hollow_thickness": self.cfg.hollow_thickness,
                "endcapremoval": self.cfg.endcap_removal,
                "freqs": self.freqs.tolist(),
                "num_freqs": self.num_freqs,
                "freq_scale": f" {self.cfg.freq_scale}",
                "enable_sparams": self.cfg.enable_sparams,
            }
            with open(setup_json, "w") as f:
                f.write(json.dumps(setup_data, indent=4))

            setup_done = self.xfproj / "Simulations" / f"{indv:06d}" / "status.dat"
            while True:
                if setup_done.exists():
                    with open(setup_done) as f:
                        content = f.read()
                    if "Created" in content:
                        print(f"Simulation created for individual {indv}.")
                        setup_json.unlink()
                        break
                time.sleep(1)

    async def sim_job(self, indv: int) -> None:
        """
        Submits and waits for XFdtd antenna simulation job to complete.

        Args:
            indv (int): current indv

        """
        sim_status = self._get_status_file(indv)

        if sim_status.exists():
            print(f"Evaluation {indv} is complete!")
            return

        running = await self._is_job_running(str(indv))
        if running:
            print(f"Evaluation {indv} is currently running!")
            await self._wait_for_completion(str(indv), sim_status)
            return

        await self.wait_for_slot(self.cfg.xf_keys)

        print(f"Submitting XF job for indv {indv}!")
        await self._submit_job(indv)
        await self._wait_for_completion(str(indv), sim_status)

    def sim_output(self, indv: int, indv_dir: Path) -> None:
        """
        Outputs Antenna simulation data from XF simulation data.

        Args:
            indv (int): Current indv
            indv_dir (Path): Path to directory for indv for output.

        Returns:
            Outputs UAN file for antenna gain + phase data and csv file with S11, VSWR, Impedance, etc. data.

        Raises:
            ValueError if output files are not able to be created.

        """
        uan_dir = indv_dir / "uan_files"
        uan_dir.mkdir(parents=True, exist_ok=True)

        out_json = self.xf_run_scripts / "output" / f"{indv}.json"
        out_data = {
            "indv_dir": str(indv_dir),
            "gaintype": self.cfg.gain_type,
            "indv_num": indv,
            "num_freqs": self.num_freqs,
        }
        with open(out_json, "w") as f:
            json.dump(out_data, f, indent=4)

        while True:
            num_files = len([f for f in uan_dir.iterdir() if f.is_file()])

            if num_files >= self.num_freqs:
                print(f"Found {num_files} files for individual {indv}.")
                out_json.unlink()
                break

        # NOTE: We have outputs, removing the simulation data to save space
        # Without this XF projects get large, quickly with data that we don't need for evolution
        # Keeping the simulation directory as to make sure that evaluations are properly kept track of for debugging in case issue.
        sim_dir = self.xfproj / "Simulations" / f"{indv:06d}"
        for item in sim_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    def _get_status_file(self, indv: int) -> Path:
        """Returns path to xfdtd status file."""
        return self.xfproj / "Simulations" / f"{indv:06d}" / "Run0001" / "output" / "status" / "runstatus.complete"

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
        job_name = str(indv)

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

    async def jobs_running(self, user: str | None = None) -> int:
        """Return number of jobs currently running or pending for the user."""
        if user is None:
            user = os.getenv("USER")
        proc = await asyncio.create_subprocess_shell(
            f"squeue -u {user} -h",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, _ = await proc.communicate()
        return len(out.decode().strip().splitlines())

    async def wait_for_slot(self, xf_keys: int, user: str | None = None, poll: int = 10) -> None:
        """Wait until the number of running jobs is below xf_keys."""
        while True:
            running = await self.jobs_running(user)
            if running < xf_keys:
                return
            print(f"{running} jobs running, waiting for free slot...")
            await asyncio.sleep(poll)

    async def persistent_xf(self) -> None:
        """Check if GUI is open, if it's not open with persistent XF script running."""
        async with self._xf_lock:
            if not is_running("xfui_exe"):
                print("Opening Persistent XF GUI")
                self.run_xfdtd(self.run_dir)


# Helper functions


class NpEncoder(json.JSONEncoder):
    """Helper class for json conversion."""

    def default(self, obj: any) -> str:
        """Properties needed for JSON conversion."""
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def rmat_to_euler(rmat: np.ndarray) -> float:
    """Converts a rotation matrix to euler angles."""
    if rmat[2][0] != 1 and rmat[2][0] != -1:
        pitch = -np.arcsin(rmat[2][0])
        heading = np.arctan2(rmat[2][1] / np.cos(pitch), rmat[2][2] / np.cos(pitch))
        roll = np.arctan2(rmat[1][0] / np.cos(pitch), rmat[0][0] / np.cos(pitch))
    else:
        roll = 0
        if rmat[2][0] == -1:
            pitch = np.pi / 2
            heading = np.arctan2(rmat[0][1], rmat[0][2])
        else:
            pitch = -np.pi / 2
            heading = np.arctan2(-rmat[0][1], -rmat[0][2])

    return heading, pitch, roll


def is_running(process_name: str) -> bool:
    """Return True if a process with the given name is running."""
    return any(proc.info["name"] == process_name for proc in psutil.process_iter(attrs=["name"]))
