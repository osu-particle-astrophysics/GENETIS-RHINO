"""Class for constructing an antenna's Phenotype and acting upon it."""
import copy
import random
from typing import Optional

from src.GENETIS_RHINO.dummy_fitness_func import DummyFitnessFunc
from src.GENETIS_RHINO.genotype import Genotype


class Phenotype:
    """
    Phenotype class.

    A wrapper for the Genotype class representing an individual antenna's
    phenotype.

    :param genotype: a Genotype instance.
    :type genotype: Genotype
    :param indiv_id: The individual's unique ID.
    :type indiv_id: str, optional
    :param parent1_id: The individual's parent's unique ID.
    :type parent1_id: str, optional
    :param generation_created: Which generation the individual was created.
    :type generation_created: int, optional
    """

    def __init__(self, genotype: Genotype,
                 indiv_id: Optional[str],
                 parent1_id: Optional[str],
                 generation_created: Optional[int]) -> None:
        """
        Phenotype constructor.

        Constructs the phenotype of a genotype.

        :param genotype: a Genotype instance.
        :type genotype: Genotype
        :param indiv_id: The individual's unique ID.
        :type indiv_id: str, optional
        :param parent1_id: The individual's parent's unique ID.
        :type parent1_id: str, optional
        :param generation_created: Which generation the individual was created.
        :type generation_created: int, optional
        :rtype: None
        """
        self.genotype = genotype
        self.indiv_id = indiv_id
        self.parent1_id = parent1_id
        self.generation_created = generation_created
        self.fitness_scores = DummyFitnessFunc(genotype).get_fitness_scores()

    def make_offspring(self, new_id: str, generation_num: int,
                       rand: random.Random) -> "Phenotype":
        """
        Make offspring.

        Makes an offspring from the individual Phenotype this is called on.

        :param new_id: The new individual's unique ID.
        :type new_id: str
        :param generation_num: The current generation number.
        :type generation_num: int
        :param rand: Random number generator object.
        :type rand: random.Random
        :rtype: None
        """
        # make a copy of parent 1 to be the offspring
        offspring = copy.deepcopy(self)

        # set fields for new individual
        offspring.parent1_id = self.indiv_id
        offspring.indiv_id = new_id
        offspring.generation_created = generation_num

        # mutate offspring
        offspring.genotype.mutate(rand)

        # calc new fitness score  TODO Replace with actual fitness calc
        offspring.fitness_scores = DummyFitnessFunc(
            offspring.genotype).get_fitness_scores()
        return offspring
