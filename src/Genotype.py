import random
from typing import Optional

from src.WallPair import WallPair

"""Class for constructing an antenna Genotype and acting upon it.

This module provides:
- generate: randomly generates a new Genotype
- mutate: mutates the Genotype
"""
class Genotype:
    """
    A class representing an individual antenna's genotype.

    :param height: The height of the antenna.
    :type height: float, optional
    :param waveguide_height: The height of the waveguide.
    :type waveguide_height: float, optional
    :param waveguide_length: The length of the waveguide.
    :type waveguide_length: float, optional
    :param walls: A list of WallPair objects that comprise the walls of the
    antenna.
    :type walls: list, optional
    """

    # Logical constraint constants  #TODO set to correct units and values
    MIN_HEIGHT = 0.0              # cm; exclusive
    MAX_HEIGHT = 100.0            # cm; inclusive

    MIN_WAVEGUIDE_HEIGHT = 0.0    # cm; exclusive
    MAX_WAVEGUIDE_HEIGHT = 100.0  # cm; inclusive

    MIN_WAVEGUIDE_LENGTH = 0.0    # cm; exclusive
    MAX_WAVEGUIDE_LENGTH = 100.0  # cm; inclusive

    def __init__(self, height: Optional[float] = None,
                 waveguide_height: Optional[float] = None,
                 waveguide_length: Optional[float] = None,
                 walls: Optional[list] = None) -> None:
        """
        The constructor for a Genotype object (an individual antenna's
        genotype).

        :param height: The height of the antenna.
        :type height: float, optional
        :param waveguide_height: The height of the waveguide.
        :type waveguide_height: float, optional
        :param waveguide_length: The length of the waveguide.
        :type waveguide_length: float, optional
        :param walls: A list of WallPair objects that comprise the walls of the
        antenna.
        :type walls: list, optional
        :rtype: None
        """

        # Make sure the list of walls provided to the constructor is valid.
        if walls is not None:
            if not all(isinstance(wall_pair, WallPair) for wall_pair in walls):
                raise ValueError("walls must be a list of WallPair objects.")

        self.height = height
        self.waveguide_height = waveguide_height
        self.waveguide_length = waveguide_length
        self.walls = walls

    def generate(self, num_wall_pairs: int, rand: random.Random):
        """
        Makes a Genotype object with randomly generated genes.

        :param num_wall_pairs: number of WallPair objects
        :param num_wall_pairs: int
        :param rand: Random number generator object.
        :type rand: random.Random
        :return: Genotype object
        :rtype: Genotype
        """

        # generate valid random height
        height = Genotype.MIN_HEIGHT
        while height == Genotype.MIN_HEIGHT: # exclude min
            height = rand.uniform(Genotype.MIN_HEIGHT, Genotype.MAX_HEIGHT)

        # generate valid random waveguide_height
        waveguide_height = Genotype.MIN_WAVEGUIDE_HEIGHT
        while waveguide_height == Genotype.MIN_WAVEGUIDE_HEIGHT: # exclude min
            waveguide_height = rand.uniform(Genotype.MIN_WAVEGUIDE_HEIGHT,
                                         Genotype.MAX_WAVEGUIDE_HEIGHT)

        # generate valid random waveguide_length
        waveguide_length = Genotype.MIN_WAVEGUIDE_LENGTH
        while waveguide_length == Genotype.MIN_WAVEGUIDE_LENGTH: # exclude min
            waveguide_length = rand.uniform(Genotype.MIN_WAVEGUIDE_LENGTH,
                                         Genotype.MAX_WAVEGUIDE_LENGTH)

        # generate list of walls with randomly generated values
        walls = WallPair().generate_list(num_wall_pairs, rand)

        return Genotype(height, waveguide_height, waveguide_length, walls)

    def mutate(self, per_site_mut_rate: float, mut_effect_size: float, rand: random.Random):
        """
        Mutates a genotype.

        :param per_site_mut_rate: The % chance any given variable in the Genotype will be mutated.
        :type per_site_mut_rate: float
        :param mut_effect_size: The mutation amplitude when a mutation takes place.
        :type mut_effect_size: float
        :param rand: Random number generator object.
        :type rand: random.Random
        :rtype: None
        """

        core_genes = ["height", "waveguide_height", "waveguide_length"]

        # Iterate over each gene in the Genotype
        for gene in core_genes:
            # if it's randomly selected to mutate, apply a mutation of
            # mut_effect_size
            if per_site_mut_rate >= rand.uniform(0, 1):
                if gene == "height":
                    self.height = self.height + rand.gauss(0,mut_effect_size)

                elif gene == "waveguide_height":
                    self.waveguide_height = (self.waveguide_height +
                                             rand.gauss(0, mut_effect_size))

                elif gene == "waveguide_length":
                    self.waveguide_length = (self.waveguide_length +
                                                rand.gauss(0, mut_effect_size))
        # TODO add WallPair mutating

    # TODO func to construct one from 1 parent

    # TODO func to construct from 2 parents with crossover -- do later

    # TODO write to CSV line
