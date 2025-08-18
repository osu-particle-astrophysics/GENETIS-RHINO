"""Class for constructing an antenna's Phenotype and acting upon it."""
from typing import Optional


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
                 generation_created: Optional[int],
                 fitness_score: Optional[float]) -> None:
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
        :param fitness_score: The fitness score of the individual.
        :type fitness_score: float, optional
        :rtype: None
        """
        self.genotype = genotype
        self.indv_id = indv_id
        self.parent_id = parent_id
        self.generation_created = generation_created
        self.fitness_score = fitness_score
