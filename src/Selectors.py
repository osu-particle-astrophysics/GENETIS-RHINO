"""Abstract selector class defines the interface for all selection algorithms."""

from abc import ABC, abstractmethod
import random

from Phenotype import Phenotype


class AbstractSelector(ABC):
    """Each selector chooses one parent from a selection pool."""

    @abstractmethod
    def select_one(self, selection_pool: list[Phenotype]) -> Phenotype: ...

class NSGATournament(AbstractSelector):
    """
    Implements binary tournament selection.

    """

    def select_one(self, selection_pool: list[Phenotype]) -> Phenotype:
        i1, i2 = random.sample(selection_pool, 2)

        # Compare rank
        if i1.nsgaii_rank < i2.nsgaii_rank:
            return i1
        elif i2.nsgaii_rank < i1.nsgaii_rank:
            return i2

        # Compare distance
        if i1.nsgaii_distance > i2.nsgaii_distance:
            return i1
        elif i2.nsgaii_distance > i1.nsgaii_distance:
            return i2

        # Randomly break ties
        return random.choice([i1, i2])
