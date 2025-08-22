import unittest
from unittest.mock import MagicMock
from src.Selectors import NSGATournament 

class MockPhenotype:
    def __init__(self, rank, distance):
        self.nsgaii_rank = rank
        self.nsgaii_distance = distance


class NSGATournamentTest(unittest.TestCase):
    """A test class to test the NSGATournament selector."""

    def setUp(self):
        """Set up the selector for tests."""
        self.selector = NSGATournament()

    def test_select_by_rank(self):
        """Tests that the individual with the better rank is selected."""
        i1 = MockPhenotype(rank=1, distance=0.5)
        i2 = MockPhenotype(rank=2, distance=1.0)

        # Mock a random generator to always return the pop from sample
        rand = MagicMock()
        rand.sample.return_value = [i1, i2]

        result = self.selector.select_one([i1, i2], rand)
        self.assertIs(result, i1)

        i1.nsgaii_rank = 3
        i2.nsgaii_rank = 1
        result = self.selector.select_one([i1, i2], rand)
        self.assertIs(result, i2)

    def test_ranks_equal(self):
        """Tests that the individual with greater distance is selected when ranks are equal."""
        i1 = MockPhenotype(rank=1, distance=0.5)
        i2 = MockPhenotype(rank=1, distance=1.0)

        rand = MagicMock()
        rand.sample.return_value = [i1, i2]

        result = self.selector.select_one([i1, i2], rand)
        self.assertIs(result, i2)

    def test_random_tie_break(self):
        """Tests that a tie in rank and distance is resolved randomly."""
        i1 = MockPhenotype(rank=1, distance=1.0)
        i2 = MockPhenotype(rank=1, distance=1.0)

        rand = MagicMock()
        rand.sample.return_value = [i1, i2]
        rand.choice.return_value = i2

        result = self.selector.select_one([i1, i2], rand)
        self.assertIs(result, i2)
        rand.choice.assert_called_once_with([i1, i2])

if __name__ == '__main__':
    unittest.main()
