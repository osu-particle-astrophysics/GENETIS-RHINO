"""File to run XFdtd simulation tests to make sure files work."""

# File paths relevant to PUEO are left in comments next to where they have been altered for reference

from pathlib import Path
import logging
import shutil
import time
import asyncio

from .xf_job import XFdtdSim

log = logging.getLogger(__name__)

# Fake settings to use for testing
npop = 10
run_dir = "/users/PAS1977/jacobweiler/GENETIS/test_repos/GENETIS-RHINO/src/xfdtd/testing"
settings = {
    "working_dir": "/users/PAS1977/jacobweiler/GENETIS/test_repos/GENETIS-RHINO",
    "freq_start": 300,
    "freq_step": 16,
    "freq_end": 600,
    "freq_scale": "MHz",
    "xf_units": "cm",
    "enable_sparams": True,
    "gain_type": "Realized",
    "xf_keys": 3,
}

# Put temporary genes for testing
genes = {
    "wg_h": 20.00,  # Waveguide height
    "wg_l": 10.00,  # Waveguide length
    "horn_h": 20.00,  # Horn height
    "horn_ang": 60,  # Horn angle #TODO: Check if radians or degrees
    "ridge_h": 0.5,  # Ridge height (%)
    "t_ridge_w": 0.6,  # top ridge width (%)
    "b_ridge_w": 0.3,  # bottom ridge width (%)
    "t_ridge_thick": 0.4,  # top ridge thickness (%)
    "b_ridge_thick": 0.3,  # bottom ridge thickness (%)
    "1_ground": [1, 0, 0],  # coordinate of feed1 ground #TODO: Is this needed?
    "1_feed": [-1, 0, 0],  # coordinate of feed1 feed
}

# Run persistent XFdtd through a generation
tasks = []
xf = XFdtdSim(run_dir, settings)
for indv in range(npop):
    indv_dir = run_dir / str(indv)
    tasks.append(xf.antenna_sim(genes, indv_dir))

await asyncio.gather(*tasks)
