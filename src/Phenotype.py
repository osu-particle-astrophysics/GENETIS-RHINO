"""Class for constructing an antenna's Phenotype and acting upon it."""
import copy
import random
from typing import Optional, Self


class Phenotype:
    """
    Phenotype class.

    A wrapper for the Genotype class representing an individual antenna's
    phenotype.

    :param genotype: a Genotype instance.
    :type genotype: Genotype
    :param indv_id: The individual's unique ID.
    :type indv_id: str, optional
    :param parent_id: The individual's parent's unique ID.
    :type parent_id: str, optional
    :param generation_created: Which generation the individual was created.
    :type generation_created: int, optional
    :param fitness_score: The fitness score of the individual.
    :type fitness_score: float, optional
    """

    def __init__(self, genotype: object,
                 indv_id: Optional[str],
                 parent_id: Optional[str],
                 generation_created: Optional[int]) -> None:
        """
        Phenotype constructor.

        Constructs the phenotype of a genotype.

        :param genotype: a Genotype instance.
        :type genotype: Genotype
        :param indv_id: The individual's unique ID.
        :type indv_id: str, optional
        :param parent_id: The individual's parent's unique ID.
        :type parent_id: str, optional
        :param generation_created: Which generation the individual was created.
        :type generation_created: int, optional
        :rtype: None
        """
        self.genotype = genotype
        self.indv_id = indv_id
        self.parent_id = parent_id
        self.generation_created = generation_created
        self.fitness_score = None # TODO replace with calc_fitness_score call

    def make_offspring(self, new_id: int, per_site_mut_rate: float, mut_effect_size: float, rand: random.Random) -> object:
        """
        Make offspring.

        Makes an offspring from the individual Genotype this is called on.

        :param per_site_mut_rate: The % chance any given variable in the Genotype will be mutated.
        :type per_site_mut_rate: float
        :param mut_effect_size: The mutation amplitude when a mutation takes place.
        :type mut_effect_size: float
        :param rand: Random number generator object.
        :type rand: random.Random
        :rtype: None
        """
        # make a copy of parent 1 to be the offspring
        offspring = copy.deepcopy(self)
        # set fields for new_indiv
        offspring.parent_id = self.indv_id
        offspring.indv_id = new_id

        # mutate offspring
        offspring.genotype.mutate(per_site_mut_rate, mut_effect_size, rand)

        return offspring
