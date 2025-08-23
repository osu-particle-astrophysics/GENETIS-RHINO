import random
import unittest

import src.Evolver as E


class MockPhenotype:
    def __init__(self, id, fitness):
        self.id = id
        self.fitness = fitness

    def make_offspring(self, new_id, rand):
        new_fit = {fitness: value+1 for fitness, value in self.fitness.items()}
        new_indiv = MockPhenotype(new_id, new_fit)
        return new_indiv


class NSGA2Test(unittest.TestCase):
    """
    A test class to test the NSGA2 evolve method.
    """

    def setUp(self):
        """Set up NSGA2 instance for tests."""
        self.nsga2 = E.NSGA2()
        self.rand = random.Random(1)
        self.population = [
            # Should be rank 1
            MockPhenotype(1, fitness={"1": 10, "2": 20, "3": 30}),
            MockPhenotype(2, fitness={"1": 20, "2": 10, "3": 30}),
            MockPhenotype(3, fitness={"1": 30, "2": 20, "3": 10}),
            # Should be rank 2
            MockPhenotype(4, fitness={"1": 100, "2": 200, "3": 300}),
            MockPhenotype(5, fitness={"1": 200, "2": 100, "3": 300}),
            # Rank 3
            MockPhenotype(6, fitness={"1": 999, "2": 999, "3": 999}),
            # Added to rank 1 to ensure a non-inf crowding distance
            MockPhenotype(7, fitness={"1": 15, "2": 15, "3": 25}),
        ]


    def test_fast_non_dominated_sort(self):
        """Tests non-dominated sorting."""
        fronts = E.fast_non_dominated_sort(self.population)
        # Always returns an empty front at the end
        assert len(fronts) == 3

        expected_fronts = [
            {1, 2, 3, 7},
            {4, 5},
            {6},
        ]

        for front, expected_ids in zip(fronts, expected_fronts):
            front_ids = {indiv.id for indiv in front}
            assert front_ids == expected_ids

        # Check no dominance within a front
        for front in fronts:
            for a in front:
                for b in front:
                    assert not (E.dominates(a, b) or E.dominates(b, a))

    def test_crowding_distance_assignment(self):
        """Tests the assignment of crowding distance to indivs in a front."""
        # Sort population into fronts
        fronts = E.fast_non_dominated_sort(self.population)

        # Assign crowding distances for each front
        for front in fronts:
            E.crowding_distance_assignment(front)

        for front in fronts:
            # All distances must be non-negative
            assert all(indiv.nsgaii_distance >= 0 for indiv in front)

            # Boundary individuals (extremes for any objective) must have inf
            for obj in front[0].fitness.keys():
                sorted_front = sorted(front, key=lambda x: x.fitness[obj])
                assert sorted_front[0].nsgaii_distance == float("inf")
                assert sorted_front[-1].nsgaii_distance == float("inf")

            # If more individuals than objectives, at least one non-boundary exists, so we have finite CD
            if len(front) > len(front[0].fitness):
                assert any(indiv.nsgaii_distance < float("inf") for indiv in front)

    def test_dominates(self):
        """Tests that the indivs in the test pop correctly dominate each other."""
        # Our first indivs in our test pop should not be dominated
        for indiv in self.population:
            for i in range(2):
                assert not E.dominates(indiv, self.population[i])
            
            # Last indiv in population should be dominated by everyone
            if indiv.id != 6:
                assert E.dominates(indiv, self.population[-2])

        # First 3 indivs should dominate indivs 4-6
        assert E.dominates(self.population[0], self.population[3])
        assert E.dominates(self.population[0], self.population[4])
        assert E.dominates(self.population[0], self.population[5])

        assert E.dominates(self.population[1], self.population[3])
        assert E.dominates(self.population[1], self.population[4])
        assert E.dominates(self.population[1], self.population[5])

        assert E.dominates(self.population[2], self.population[3])
        assert E.dominates(self.population[2], self.population[4])
        assert E.dominates(self.population[2], self.population[5])

if __name__ == '__main__':
    unittest.main()
