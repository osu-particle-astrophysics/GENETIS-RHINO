"""Abstract selector class defines the interface for all selection algorithms."""

import random
from abc import ABC, abstractmethod

from src.Phenotype import Phenotype


class AbstractSelector(ABC):
    """Each selector chooses one parent from a selection pool."""

    @abstractmethod
    def select_one(self, selection_pool: list[Phenotype], rand: random.Random) -> Phenotype:
        """Given a list of Phenotype objects, select on to be a parent."""


class NSGATournament(AbstractSelector):
    """Implements binary tournament selection."""

    def select_one(self, selection_pool: list[Phenotype], rand: random.Random) -> Phenotype:
        """Choose between two random individuals based on rank, then crowding distance."""
        i1, i2 = rand.sample(selection_pool, 2)

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
        return rand.choice([i1, i2])
