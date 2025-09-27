"""antenna_fitness.py simulates antennas then calculates antenna fitness"""

import asyncio
from pathlib import Path

from src.GENETIS_RHINO.parameters import ParametersObject
from src.GENETIS_RHINO.phenotype import Phenotype
from src.GENETIS_RHINO.fitness_functions import calculate_fitnesses
from src.xfdtd.xf_job import XFdtdSim


async def antenna_performance(run_dir: Path, cfg: ParametersObject, indv: Phenotype):
    """Simulates antenna then calculates fitness"""
    # Simulate in XFdtd
    xf = XFdtdSim(run_dir, cfg)
    indv_uan_dir = await xf.antenna_sim(int(indv.indiv_id) + 1, indv.genotype)
    # TODO: I make this +1 because XF requires ID to start from 1
    await asyncio.sleep(1)

    # Calculate + Update Fitness
    indv.fitness_scores = calculate_fitnesses(indv_uan_dir)
