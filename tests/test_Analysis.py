import random
import unittest
import pathlib

from src.GENETIS_RHINO.analysis import Analysis
from src.GENETIS_RHINO.genotype import Genotype
from src.GENETIS_RHINO.parameters import ParametersObject
from src.GENETIS_RHINO.phenotype import Phenotype

cfg = ParametersObject(str(pathlib.Path(
    __file__).parent.parent/"src/GENETIS_RHINO/config.toml"))

class AnalysisTest(unittest.TestCase):
    """A test class to test the Analysis class."""

    @staticmethod
    def make_analysis(population_size: int) -> Analysis:
        """Make a population of Phenotypes to be used by other test methods in this class."""
        r = random.randint
        genotypes = [Genotype(cfg).generate_without_ridge(random.Random(1)) for _ in
                     range(population_size)]
        phenotypes = [Phenotype(g, "Evan", "None", 0) for g in genotypes]
        for p in phenotypes:
            p.nsgaii_rank = r(0,10)
            p.fitness_scores = {"metric1": r(0, 10),
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
        lowest_rank = min(indiv.nsgaii_rank for indiv in analysis.population)
        best_indivs = analysis.update_best_individuals()
        # Test that at least one best individual is found.
        self.assertGreaterEqual(len(best_indivs), 1)
        for best_indiv in best_indivs:
            for indiv in analysis.population:
                # Test that all best individuals have the same nsgaii rank.
                self.assertEqual(best_indiv.nsgaii_rank, lowest_rank)
                self.assertLessEqual(best_indiv.nsgaii_rank, indiv.nsgaii_rank)

    def test_update_fitness(self) -> None:
        """Test that fitness statistics for a population generation are recorded correctly."""
        analysis = self.make_analysis(10)
        fitness_table = analysis.update_fitness_scores()
        metrics = analysis.population[0].fitness_scores.keys()
        # Test that all the statistics were recorded.
        self.assertEqual(len(fitness_table), len(metrics)*2+1)
        for metric in metrics:
            scores = [indiv.fitness_scores[metric] for indiv in
                      analysis.population]
            avg_score = sum(scores) / len(scores)
            max_score = max(scores)
            # Test that the average and maximum values are calculated as expected.
            self.assertEqual(fitness_table[metric+"_Average"][0], avg_score)
            self.assertEqual(fitness_table[metric+"_Maximum"][0], max_score)
        print(len(fitness_table))

if __name__ == '__main__':
    unittest.main()