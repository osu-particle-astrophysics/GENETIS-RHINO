import unittest
from random import Random
import pathlib

from src.GENETIS_RHINO.genotype import Genotype
from src.GENETIS_RHINO.manager import Manager
from src.GENETIS_RHINO.parameters import ParametersObject
from src.GENETIS_RHINO.phenotype import Phenotype


class test_Manager(unittest.TestCase):
    """
    A test class to test the Manager class.
    """
    # Constants for all tests
    SEED = 1  # random number generator seed
    POPULATION_SIZE = 2
    PER_SITE_MUT_RATE = 1.0  # per site mutation rate
    MUT_AMPLITUDE = 0.1  # mutation amplitude

    # config for all tests
    cfg = ParametersObject(str(pathlib.Path(
        __file__).parent.parent / "src/GENETIS_RHINO/config.toml"))
    cfg.population_size = 2
    cfg.per_site_mut_rate = PER_SITE_MUT_RATE
    cfg.mut_effect_size = MUT_AMPLITUDE

    def test_constructor(self):
        """
        Tests the Manager constructor with valid inputs.
        """
        manager = Manager(self.cfg)

        self.assertEqual(manager.seed, self.SEED)
        self.assertIsInstance(manager.rand, Random)
        self.assertIsInstance(manager.population, list)

    def test_initialize_population(self):
        """Test initializing a new random population"""
        manager = Manager(self.cfg)
        manager.initialize_population(self.cfg)

        self.assertIsInstance(manager.population, list)
        self.assertIsInstance(manager.population[0], Phenotype)

        p = manager.population[0]
        self.assertIsInstance(p.genotype, Genotype)
        self.assertEqual(p.indiv_id, "0")
        self.assertEqual(p.parent1_id, "None")
        self.assertEqual(p.generation_created, 0)
        self.assertEqual(p.fitness_scores, {
            'flare_length': 2.4030927323372038,
            'waveguide_height': 877.9469895497862,
            'waveguide_length': 787.3971570789527,
            'waveguide_width': 329.56212316547953,
            'wp0_angle': 44.58915783827469,
            'wp0_ridge_height': 44.949106478873816,
            'wp0_ridge_thickness_bottom': 2.834747652200631,
            'wp0_ridge_thickness_top': 9.385958677423488,
            'wp0_ridge_width_bottom': 78.87233511355132,
            'wp0_ridge_width_top': 65.15929727227629,
            'wp1_angle': 75.21885935278827,
            'wp1_ridge_height': 43.27670679050534,
            'wp1_ridge_thickness_bottom': 72.15400323407826,
            'wp1_ridge_thickness_top': 44.538719405480144,
            'wp1_ridge_width_bottom': 0.21060533511106927,
            'wp1_ridge_width_top': 76.2280082457942})

    def test_evolve_one_gen(self):
        """Test evolving one generation"""
        manager = Manager(self.cfg)
        manager.initialize_population(self.cfg)
        manager.evolve_one_gen(1)
        self.assertIsInstance(manager.population, list)
        self.assertIsInstance(manager.population[0], Phenotype)

        p = manager.population[0]
        self.assertEqual(p.indiv_id, "2")
        self.assertEqual(p.parent1_id, "1")
        self.assertEqual(p.generation_created, 1)
        self.assertEqual(p.fitness_scores, {
            'flare_length': 2.4937490423322344,
            'waveguide_height': 956.328504573443,
            'waveguide_length': 911.1744514610525,
            'waveguide_width': 127.41452188959455,
            'wp0_angle': 2.503369724015581,
            'wp0_ridge_height': 53.97707099277368,
            'wp0_ridge_thickness_bottom': 42.19212615825646,
            'wp0_ridge_thickness_top': 21.77593956910127,
            'wp0_ridge_width_bottom': 42.19212615825646,
            'wp0_ridge_width_top': 93.69562915854259,
            'wp1_angle': 2.6828107724558463,
            'wp1_ridge_height': 22.07802423049017,
            'wp1_ridge_thickness_bottom': 23.044241536772077,
            'wp1_ridge_thickness_top': 23.305298856196707,
            'wp1_ridge_width_bottom': 23.044241536772077,
            'wp1_ridge_width_top': 43.739935107584955})


if __name__ == '__main__':
    unittest.main()