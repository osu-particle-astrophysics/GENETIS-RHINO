import random
import unittest
import pathlib

from src.GENETIS_RHINO.phenotype import Genotype
from src.GENETIS_RHINO.parameters import ParametersObject
from src.GENETIS_RHINO.phenotype import Phenotype

cfg = ParametersObject(str(pathlib.Path(
        __file__).parent.parent/"src/GENETIS_RHINO/config.toml"))

class PhenotypeTest(unittest.TestCase):
    """
    A test class to test the Phenotype class.
    """

    def test_constructor(self):
        """
        Tests the Phenotype constructor with valid inputs.
        """
        # Build a valid Genotype object.
        g = Genotype(cfg).generate_with_ridge(random.Random(1))

        # Build a valid Phenotype object.
        p = Phenotype(g, "Kate", "None", 0)

        self.assertIsInstance(p.genotype, Genotype)
        self.assertEqual(p.indiv_id, "Kate")
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

    def test_make_offspring(self):
        """Tests the make_offspring function."""
        # build valid parent phenotype
        g = Genotype(cfg).generate_without_ridge(random.Random(1))
        parent = Phenotype(g, "Kate", "None", 0)

        # make a single offspring via asexual reproduction
        child = parent.make_offspring("Oona", 1, random.Random(1))

        self.assertIsInstance(child.genotype, Genotype)
        self.assertEqual(child.indiv_id, "Oona")
        self.assertEqual(child.parent1_id, "Kate")
        self.assertEqual(child.generation_created, 1)
        self.assertEqual(child.fitness_scores, {
            'wp0_angle': 44.58915783827469,
            'wp1_angle': 75.21885935278827,
            'flare_length': 2.5007170272643924,
            'wp0_ridge_height': 44.949106478873816,
            'wp1_ridge_height': 43.27670679050534,
            'wp0_ridge_thickness_bottom': 2.8684239590974654,
            'wp1_ridge_thickness_bottom': 72.15400323407826,
            'wp0_ridge_thickness_top': 9.385958677423488,
            'wp1_ridge_thickness_top': 44.31006947870848,
            'wp0_ridge_width_bottom': 2.8684239590974654,
            'wp1_ridge_width_bottom': 0.13803132555967296,
            'wp0_ridge_width_top': 65.34636693312109,
            'wp1_ridge_width_top': 76.43067117717526,
            'waveguide_height': 877.807961223367,
            'waveguide_length': 787.3971570789527,
            'waveguide_width': 329.56212316547953})

if __name__ == '__main__':
    unittest.main()
