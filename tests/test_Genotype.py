import unittest
import random
import pathlib

from src.GENETIS_RHINO.genotype import Genotype
from src.GENETIS_RHINO.parameters import ParametersObject
from src.GENETIS_RHINO.wall_pair import WallPair


class GenotypeTest(unittest.TestCase):
    """Tester class for the WallPair class."""
    # Constants for all tests
    SEED = 1                 # random number generator seed
    PER_SITE_MUT_RATE = 1.0  # per site mutation rate
    MUT_AMPLITUDE = 0.1      # mutation amplitude

    # config for all tests
    cfg = ParametersObject(str(pathlib.Path(
        __file__).parent.parent / "src/GENETIS_RHINO/config.toml"))
    cfg.per_site_mut_rate = PER_SITE_MUT_RATE
    cfg.mut_effect_size = MUT_AMPLITUDE

    def test_constructor(self):
        """Tests the Genotype constructor with valid inputs."""
        # Make a list of 2 WallPair objects
        rand = random.Random(self.SEED)
        walls = WallPair(self.cfg).generate_walls_with_ridge(rand)

        # Build genotype
        g = Genotype(self.cfg, 1.0,2.0,3.0, 4.0, walls)

        self.assertEqual(g.flare_length, 1)
        self.assertEqual(g.waveguide_height, 2)
        self.assertEqual(g.waveguide_length, 3)
        self.assertEqual(g.waveguide_width, 4)
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
            Genotype(self.cfg, 1, 2, 3, 4, walls)

    def test_generate(self):
        """Tests Genotype generation with valid inputs."""
        rand = random.Random(GenotypeTest.SEED)
        g = Genotype(self.cfg).generate_with_ridge(rand)

        self.assertEqual(g.flare_length, 2.4030927323372038)
        self.assertEqual(g.waveguide_height, 877.9469895497862)
        self.assertEqual(g.waveguide_length, 787.3971570789527)
        self.assertEqual(g.waveguide_width, 329.56212316547953)
        self.assertIsInstance(g.walls[0], WallPair)

    def test_mutate(self):
        """Tests the mutate method."""
        rand = random.Random(self.SEED)
        g = Genotype(self.cfg).generate_without_ridge(rand)
        g.mutate(rand)

        self.assertEqual(g.flare_length, 2.605755663718255)
        self.assertEqual(g.waveguide_height, 877.8744155402347)
        self.assertEqual(g.waveguide_length, 787.168507152181)
        self.assertEqual(g.waveguide_width, 329.5012478420334)


if __name__ == '__main__':
    unittest.main()
