import random
import unittest
from src.WallPair import WallPair


class WallPairTest(unittest.TestCase):
    """
    A test class to test the WallPair class.
    """

    # Random number seed for all tests
    SEED = 1

    def test_constructor(self):
        """Tests the WallPair constructor when building a valid WallPair object.
        """
        wp = WallPair(1.0, 2.0, 3.0,4.0,5.0)

        self.assertEqual(wp.has_ridge, False)
        self.assertEqual(wp.width, 1)
        self.assertEqual(wp.angle, 2)
        self.assertEqual(wp.ridge_height, 3)
        self.assertEqual(wp.ridge_width, 4)
        self.assertEqual(wp.ridge_thickness, 5)

    def test_generate_without_ridge(self):
        """Tests the generate_without_ridge method which randomly generates a
        WallPair without a ridge.
        """
        rand = random.Random(WallPairTest.SEED)
        wp = WallPair().generate_without_ridge(rand)

        self.assertEqual(wp.has_ridge, False)
        self.assertEqual(wp.width, 13.436424411240122)
        self.assertEqual(wp.angle, 84.74337369372327)
        self.assertEqual(wp.ridge_height, 76.3774618976614)
        self.assertEqual(wp.ridge_width, 25.50690257394217)
        self.assertEqual(wp.ridge_thickness, 49.54350870919409)



    def test_generate_with_ridge(self):
        """Tests the generate_with_ridge method which randomly generates a
        WallPair with a ridge.
        """
        rand = random.Random(WallPairTest.SEED)
        wp = WallPair().generate_with_ridge(rand)

        self.assertEqual(wp.has_ridge, True)
        self.assertEqual(wp.width, 13.436424411240122)
        self.assertEqual(wp.angle, 84.74337369372327)
        self.assertEqual(wp.ridge_height, 76.3774618976614)
        self.assertEqual(wp.ridge_width, 25.50690257394217)
        self.assertEqual(wp.ridge_thickness, 49.54350870919409)

    def test_generate_list(self):
        """Tests the generate_list method for generating a list of
        randomly generated WallPair objects.
        """
        rand = random.Random(WallPairTest.SEED)
        walls = WallPair().generate_list(2, rand)

        self.assertEqual(len(walls), 2)
        self.assertIsInstance(walls[0], WallPair)
        self.assertIsInstance(walls[1], WallPair)

if __name__ == '__main__':
    unittest.main()
