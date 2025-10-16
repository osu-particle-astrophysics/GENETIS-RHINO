#!/bin/bash
## XFdtd simulation job script.
#SBATCH -A PAS1960
#SBATCH -N 1
#SBATCH -n 40
#SBATCH -G 2
#SBATCH -t 02:00:00
#SBATCH --mem-per-gpu=178gb

module load xfdtd/7.11.0.3
module load cuda/12.6.2

licensecheck=0
simulationcheck=0
while [ $simulationcheck -eq 0 ] || [ $licensecheck -eq 0 ]; do  
    cd "$sim_dir" || exit 1
    echo "Running XF solver"
    xfsolver --use-xstream=true --xstream-use-number=2 --num-threads=2 -v

    cd "$joboutdir" || exit 1

    if grep -q "Unable to check out license." "XFdtd_${SLURM_JOB_ID}.output" 2>/dev/null; then
        echo "Unable to check out license."
        echo "Rerunning simulation"
        cp "XFdtd_${SLURM_JOB_ID}.output" "XFdtd_${SLURM_JOB_ID}_license_err.output"
        : > "XFdtd_${SLURM_JOB_ID}.output"
    else
        echo "License checked out"
        licensecheck=1
    fi

    if grep -q "Unstable calculation detected. Terminating XFSolver." "XFdtd_${SLURM_JOB_ID}.output" 2>/dev/null; then
        echo "Unstable calculation detected. Terminating XFSolver."
        echo "Rerunning simulation"
        cp "XFdtd_${SLURM_JOB_ID}.output" "XFdtd_${SLURM_JOB_ID}_err.output"
        : > "XFdtd_${SLURM_JOB_ID}.output"
    else
        echo "Simulation finished"
        simulationcheck=1
    fi
done