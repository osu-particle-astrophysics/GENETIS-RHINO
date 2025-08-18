import unittest
import random

from src.Genotype import Genotype
from src.WallPair import WallPair


class GenotypeTest(unittest.TestCase):
    """Tester class for the WallPair class."""
    # Constants for all tests
    SEED = 1                 # random number generator seed
    PER_SITE_MUT_RATE = 0.3  # per site mutation rate
    MUT_AMPLITUDE = 0.1      # mutation amplitude

    def test_constructor(self):
        """Tests the Genotype constructor with valid inputs."""
        # Make a list of 2 WallPair objects
        rand = random.Random(self.SEED)
        walls = WallPair().generate_list(2, rand)

        # Build genotype
        g = Genotype(1.0,2.0,3.0, walls)

        self.assertEqual(g.height, 1)
        self.assertEqual(g.waveguide_height, 2)
        self.assertEqual(g.waveguide_length, 3)
        self.assertIsInstance(g.walls[0], WallPair)
        self.assertIsInstance(g.walls[1], WallPair)

    def test_constructor_invalid_items_in_walls_list(self):
        """Tests the Genotype constructor error catching with invalid wall
        list.
        """
        # Make a list of ints
        walls = [0] * 2

        # Build genotype and make sure the error is raised
        with self.assertRaises(ValueError):
            Genotype(1, 2, 3, walls)

    def test_generate(self):
        """Tests Genotype generation with valid inputs."""
        rand = random.Random(GenotypeTest.SEED)
        g = Genotype().generate(2, rand)

        self.assertEqual(g.height, 13.436424411240122)
        self.assertEqual(g.waveguide_height, 84.74337369372327)
        self.assertEqual(g.waveguide_length, 76.3774618976614)
        self.assertIsInstance(g.walls[0], WallPair)
        self.assertIsInstance(g.walls[1], WallPair)

    def test_mutate(self):
        """Tests the mutate method."""
        rand = random.Random(self.SEED)
        g = Genotype().generate(2, rand)
        g.mutate(GenotypeTest.PER_SITE_MUT_RATE,
                 GenotypeTest.MUT_AMPLITUDE, rand)

        self.assertEqual(g.height, 13.285841511114047)
        self.assertEqual(g.waveguide_height, 84.79717341158937)
        self.assertEqual(g.waveguide_length, 76.3774618976614)

if __name__ == '__main__':
    unittest.main()
