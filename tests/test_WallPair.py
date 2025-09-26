import random
import unittest
import pathlib

from src.GENETIS_RHINO.parameters import ParametersObject
from src.GENETIS_RHINO.wall_pair import WallPair


class WallPairTest(unittest.TestCase):
    """
    A test class to test the WallPair class.
    """

    # Random number seed for all tests
    SEED = 1
    PER_SITE_MUT_RATE = 1.0  # per site mutation rate
    MUT_AMPLITUDE = 0.1  # mutation amplitude

    # config for all tests
    cfg = ParametersObject(str(pathlib.Path(
        __file__).parent.parent/"src/GENETIS_RHINO/config.toml"))
    cfg.per_site_mut_rate = PER_SITE_MUT_RATE
    cfg.mut_effect_size = MUT_AMPLITUDE

    def test_constructor(self):
        """Tests the WallPair constructor when building a valid WallPair object.
        """
        wp = WallPair(self.cfg,1.0, 2.0, 3.0,4.0,5.0, 6.0)

        self.assertEqual(wp.has_ridge, False)
        self.assertEqual(wp.angle, 1)
        self.assertEqual(wp.ridge_height, 2)
        self.assertEqual(wp.ridge_width_top, 3)
        self.assertEqual(wp.ridge_width_bottom, 4)
        self.assertEqual(wp.ridge_thickness_top, 5)
        self.assertEqual(wp.ridge_thickness_bottom, 6)

    def test_generate_without_ridge(self):
        """Tests the generate_without_ridge method which randomly generates a
        WallPair without a ridge.
        """
        rand = random.Random(WallPairTest.SEED)
        wp = WallPair(self.cfg).generate_without_ridge(rand)

        self.assertEqual(wp.has_ridge, False)
        self.assertEqual(wp.angle, 12.09278197011611)
        self.assertEqual(wp.ridge_height, 84.74337369372327)
        self.assertEqual(wp.ridge_width_top, 76.3774618976614)
        self.assertEqual(wp.ridge_width_bottom, 25.50690257394217)
        self.assertEqual(wp.ridge_thickness_top, 49.54350870919409)
        self.assertEqual(wp.ridge_thickness_bottom, 44.949106478873816)

    def test_generate_with_ridge(self):
        """Tests the generate_with_ridge method which randomly generates a
        WallPair with a ridge.
        """
        rand = random.Random(WallPairTest.SEED)
        wp = WallPair(self.cfg).generate_with_ridge(rand)

        self.assertEqual(wp.has_ridge, True)
        self.assertEqual(wp.angle, 12.09278197011611)
        self.assertEqual(wp.ridge_height, 84.74337369372327)
        self.assertEqual(wp.ridge_width_top, 76.3774618976614)
        self.assertEqual(wp.ridge_width_bottom, 25.50690257394217)
        self.assertEqual(wp.ridge_thickness_top, 49.54350870919409)
        self.assertEqual(wp.ridge_thickness_bottom, 44.949106478873816)

    def test_generate_list(self):
        """Tests the generate_list method for generating a list of
        randomly generated WallPair objects.
        """
        rand = random.Random(WallPairTest.SEED)
        walls = WallPair(self.cfg).generate_walls_with_ridge(rand)

        self.assertEqual(len(walls), 2)
        self.assertIsInstance(walls[0], WallPair)
        self.assertIsInstance(walls[1], WallPair)
        
    def test_mutate(self):
        """Tests the mutate method."""
        rand = random.Random(WallPairTest.SEED)
        wp = WallPair(self.cfg).generate_with_ridge(rand)
        
        self.assertEqual(wp.angle, 12.09278197011611)
        self.assertEqual(wp.ridge_height, 84.74337369372327)
        self.assertEqual(wp.ridge_width_top, 76.3774618976614)
        self.assertEqual(wp.ridge_width_bottom, 25.50690257394217)
        self.assertEqual(wp.ridge_thickness_top, 49.54350870919409)
        self.assertEqual(wp.ridge_thickness_bottom, 44.949106478873816)

if __name__ == '__main__':
    unittest.main()
