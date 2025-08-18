import unittest
from src.Genotype import Genotype
from src.Phenotype import Phenotype
from src.WallPair import WallPair


class PhenotypeTest(unittest.TestCase):
    def test_constructor(self):
        """
        Tests the Phenotype constructor with valid inputs.
        """
        # Make a list of 8 WallPair objects
        walls = [WallPair(4, 4) for _ in range(8)]

        # Build a valid Genotype object
        g = Genotype(1,2,3, walls)

        # Build a valid Phenotype object.
        p = Phenotype(g, "Kate", "None1", "None2", 1,2)

        self.assertEqual(p.genotype.height, 1)
        self.assertEqual(p.id, "Kate")
        self.assertEqual(p.parent1_id, "None1")
        self.assertEqual(p.parent2_id, "None2")
        self.assertEqual(p.generation_created, 1)
        self.assertEqual(p.fitness_score, 2)


    def test_constructor_invalid_genotype(self):
        """
        Tests the Phenotype constructor error catching when genotype isn't a valid Genotype object.
        """
        with self.assertRaises(TypeError):
            Phenotype("I'm not a genotype object", "Kate", "None1", "None2", 1,2)


    def test_constructor_invalid_parents(self):
        """
        Tests the Phenotype constructor error catching when parents are invalid (only 1 parent).
        """
        with self.assertRaises(ValueError):
            # Make a list of 8 WallPair objects
            walls = [WallPair(4, 4) for _ in range(8)]

            # Build a valid Genotype object
            g = Genotype(1, 2, 3, walls)

            # Build an invalid Phenotype object (only 1 parent).
            Phenotype(g, "Kate", "None1", "Dad",1, 2)


if __name__ == '__main__':
    unittest.main()
