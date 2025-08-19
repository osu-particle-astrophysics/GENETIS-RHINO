import random
import unittest

from src.Analysis import Analysis
from src.Genotype import Genotype
from src.Parameters import ParametersObject
from src.Phenotype import Phenotype

cfg = ParametersObject("src/config.toml")

class AnalysisTest(unittest.TestCase):
    """A test class to test the Analysis class."""

    def make_analysis(self, population_size: int) -> Analysis:
        """Make a population of Phenotypes to be used by other test methods in this class."""
        g = Genotype(cfg).generate(2, random.Random(1))
        # Build a valid Phenotype object.
        p = Phenotype(g, "Jessie", "None", 0)
        p = Phenotype(g, "James", "None", 0)

        r = random.randint
        genotypes = [Genotype().generate(2, random.Random(1)) for _ in range(population_size)]
        phenotypes = [Phenotype(g, "Evan", "None", 0) for g in genotypes]
        for p in phenotypes:
            p.nsgaii_rank = r(0,10)
            p.fitness_score = {"metric1": r(0,10),
                            "metric2": r(0,10),
                            "metric3": r(0,10)}

        return Analysis(phenotypes)

    def test_constructor(self) -> None:
        """Tests the Analysis constructor with valid inputs."""
        pop_size = random.randint(2, 15)
        analysis = self.make_analysis(pop_size)

        self.assertEqual(len(analysis.population), pop_size)
        
    def test_update_best_individual(self) -> None:
        """Test that the individuals with the lowest nsgaii rank are found (on the pareto front)."""
        analysis = self.make_analysis(10)
        lowest_rank = min(indv.nsgaii_rank for indv in analysis.population)
        best_indvs = analysis.update_best_individual()
        # Test that at least one best individual is found.
        self.assertGreaterEqual(len(best_indvs), 1)
        for best_indv in best_indvs:
            for indv in analysis.population:
                # Test that all best individuals have the same nsgaii rank.
                self.assertEqual(best_indv.nsgaii_rank, lowest_rank)
                self.assertLessEqual(best_indv.nsgaii_rank, indv.nsgaii_rank)

    def test_update_fitness(self) -> None:
        """Test that fitness statistics for a population generation are recorded correctly."""
        analysis = self.make_analysis(10)
        fitness_table = analysis.update_fitness()
        metrics = analysis.population[0].fitness_score.keys()
        # Test that all the statistics were recorded.
        self.assertEqual(len(fitness_table), len(metrics)*2+1)
        for metric in metrics:
            scores = [indv.fitness_score[metric] for indv in analysis.population]
            avg_score = sum(scores) / len(scores)
            max_score = max(scores)
            # Test that the average and maximum values are calculated as expected.
            self.assertEqual(fitness_table[metric+"_Average"][0], avg_score)
            self.assertEqual(fitness_table[metric+"_Maximum"][0], max_score)
        print(len(fitness_table))
