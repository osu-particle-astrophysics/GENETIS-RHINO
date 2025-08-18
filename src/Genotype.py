"""
Class for constructing an antenna Genotype and acting upon it.

This module provides:
- generate: randomly generates a new Genotype
- mutate: mutates the Genotype
"""
import random
from typing import Optional

from src.WallPair import WallPair


class Genotype:
    """
    Genotype class.

    A class representing an individual antenna's genotype.

    :param height: The height of the antenna in lambda.
    :type height: float, optional
    :param waveguide_height: The height of the waveguide.
    :type waveguide_height: float, optional
    :param waveguide_length: The length of the waveguide.
    :type waveguide_length: float, optional
    :param walls: A list of WallPair objects that comprise the walls of the
    antenna.
    :type walls: list, optional
    """

    # Logical constraint constants
    MIN_HEIGHT = 2.0                # lambda; inclusive
    MAX_HEIGHT = 5.0                # lambda; inclusive

    MIN_WAVEGUIDE_HEIGHT = 200.0    # cm; inclusive -- func of min freq you
    # care about picking up
    MAX_WAVEGUIDE_HEIGHT = 1000.0   # cm; inclusive; also not bigger than
    # aperture (in line check) #TODO

    MIN_WAVEGUIDE_LENGTH = 100.0    # cm; inclusive
    MAX_WAVEGUIDE_LENGTH = 1000.0   # cm; inclusive

    def __init__(self, height: Optional[float] = None,
                 waveguide_height: Optional[float] = None,
                 waveguide_length: Optional[float] = None,
                 walls: Optional[list] = None) -> None:
        """
        Genotype Constructor.

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
        if walls is not None and not all(isinstance(wall_pair, WallPair) for wall_pair in walls):
            raise ValueError("walls must be a list of WallPair objects.")

        self.height = height
        self.waveguide_height = waveguide_height
        self.waveguide_length = waveguide_length
        self.walls = walls

    def generate(self, num_wall_pairs: int, rand: random.Random) -> object:
        """
        Generate Genotype.

        Makes a Genotype object with randomly generated genes.

        :param num_wall_pairs: number of WallPair objects
        :param num_wall_pairs: int
        :param rand: Random number generator object.
        :type rand: random.Random
        :return: Genotype object
        :rtype: Genotype
        """
        # generate valid random height
        height = rand.uniform(Genotype.MIN_HEIGHT, Genotype.MAX_HEIGHT)

        # generate valid random waveguide_height
        waveguide_height = rand.uniform(Genotype.MIN_WAVEGUIDE_HEIGHT,
                                         Genotype.MAX_WAVEGUIDE_HEIGHT)

        # generate valid random waveguide_length
        waveguide_length = rand.uniform(Genotype.MIN_WAVEGUIDE_LENGTH,
                                         Genotype.MAX_WAVEGUIDE_LENGTH)

        # generate list of walls with randomly generated values
        walls = WallPair().generate_list(num_wall_pairs, rand)

        return Genotype(height, waveguide_height, waveguide_length, walls)

    def mutate(self, per_site_mut_rate: float, mut_effect_size: float,
               rand: random.Random) -> None:
        """
        Mutate Genotype.

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
                    # TODO check to make sure it's still within min/max vals

                elif gene == "waveguide_height":
                    self.waveguide_height = (self.waveguide_height +
                                             rand.gauss(0, mut_effect_size))
                    # TODO check to make sure it's still within min/max vals

                elif gene == "waveguide_length":
                    self.waveguide_length = (self.waveguide_length +
                                                rand.gauss(0, mut_effect_size))
                    # TODO check to make sure it's still within min/max vals

        # TODO add WallPair mutating (all)

    # TODO KATE - func to construct from 2 parents with crossover (not for v1)

    # TODO ALEX - func to write Genotype genes to CSV line
