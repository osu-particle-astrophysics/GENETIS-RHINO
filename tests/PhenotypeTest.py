import random
import unittest

from src.Genotype import Genotype
from src.Phenotype import Phenotype
from src.WallPair import WallPair


class PhenotypeTest(unittest.TestCase):
    """
    A test class to test the Phenotype class.
    """

    def test_constructor(self):
        """
        Tests the Phenotype constructor with valid inputs.
        """
        g = Genotype().generate(2, random.Random(1))

        # Build a valid Phenotype object.
        p = Phenotype(g, "Kate", "None", 0)

        self.assertIsInstance(p.genotype, Genotype)
        self.assertEqual(p.indv_id, "Kate")
        self.assertEqual(p.parent_id, "None")
        self.assertEqual(p.generation_created, 0)
        self.assertEqual(p.fitness_score, None)


if __name__ == '__main__':
    unittest.main()
