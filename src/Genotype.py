"""
Class for constructing an antenna Genotype and acting upon it.

This module provides:
- generate: randomly generates a new Genotype
- mutate: mutates the Genotype
"""
import random
from typing import Optional

from src.Parameters import ParametersObject
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

    # TODO constants should all be read in fron config instead of hardcoded
    #  here

    MIN_WAVEGUIDE_HEIGHT = 200.0    # cm; inclusive -- func of min freq you
    # care about picking up
    MAX_WAVEGUIDE_HEIGHT = 1000.0   # cm; inclusive; # TODO also prevent being
    # bigger than aperture (in line check somewhere, not here)

    MIN_WAVEGUIDE_LENGTH = 100.0    # cm; inclusive
    MAX_WAVEGUIDE_LENGTH = 1000.0   # cm; inclusive

    def __init__(self, cfg: ParametersObject,
                 height: Optional[float] = None,
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
        self.cfg = cfg

        # Logical constraint constants
        self.MAX_HEIGHT = cfg.MAX_HEIGHT
        self.MIN_HEIGHT = cfg.MIN_HEIGHT

        # cm; inclusive
        self.MIN_WAVEGUIDE_LENGTH = cfg.MIN_WAVEGUIDE_LENGTH
        self.MAX_WAVEGUIDE_LENGTH = cfg.MAX_WAVEGUIDE_LENGTH

        self.MIN_WAVEGUIDE_HEIGHT = cfg.MIN_WAVEGUIDE_HEIGHT # cm; inclusive -- func of min freq you
    # care about picking up
        self.MAX_WAVEGUIDE_HEIGHT = cfg.MAX_WAVEGUIDE_HEIGHT # cm; inclusive; # TODO also prevent being
    # bigger than aperture (in line check somewhere, not here)

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
        height = rand.uniform(self.MIN_HEIGHT, self.MAX_HEIGHT)

        # generate valid random waveguide_height
        waveguide_height = rand.uniform(self.MIN_WAVEGUIDE_HEIGHT,
                                         self.MAX_WAVEGUIDE_HEIGHT)

        # generate valid random waveguide_length
        waveguide_length = rand.uniform(self.MIN_WAVEGUIDE_LENGTH,
                                         self.MAX_WAVEGUIDE_LENGTH)

        # generate list of walls with randomly generated values
        walls = WallPair().generate_list(num_wall_pairs, rand)

        return Genotype(self.cfg, height, waveguide_height, waveguide_length, walls)

    def mutate(self, rand: random.Random) -> None:
        """
        Mutate Genotype.

        Mutates a genotype.

        :param rand: Random number generator object.
        :type rand: random.Random
        :rtype: None
        """
        per_site_mut_rate = self.cfg.per_site_mut_rate
        mut_effect_size = self.cfg.mut_effect_size

        core_genes = ["height", "waveguide_height", "waveguide_length"]

        # Iterate over each gene in the Genotype
        for gene in core_genes:
            # if it's randomly selected to mutate, apply a mutation of
            # mut_effect_size in Guassian distribution
            if per_site_mut_rate >= rand.uniform(0, 1):
                # height gene
                if gene == "height":
                    self.height = self.height + rand.gauss(0,mut_effect_size)
                    # if under min bound, set to min
                    self.height = max(self.height, self.MIN_HEIGHT)
                    # if over max bound, set to max
                    self.height = min(self.height, self.MAX_HEIGHT)

                # waveguide_height gene
                elif gene == "waveguide_height":
                    self.waveguide_height = (self.waveguide_height +
                                             rand.gauss(0, mut_effect_size))
                    # if under min bound, set to min
                    self.waveguide_height = max(self.waveguide_height,
                                                self.MIN_WAVEGUIDE_HEIGHT)
                    # if over max bound, set to max
                    self.waveguide_height = min(self.waveguide_height, self.MAX_WAVEGUIDE_HEIGHT)

                # waveguide_length gene
                elif gene == "waveguide_length":
                    self.waveguide_length = (self.waveguide_length +
                                                rand.gauss(0, mut_effect_size))
                    # if under min bound, set to min
                    self.waveguide_length = max(self.waveguide_length, self.MIN_WAVEGUIDE_LENGTH)
                    # if over of max bound, set to max
                    self.waveguide_length = min(self.waveguide_length, self.MAX_WAVEGUIDE_LENGTH)
        # mutate the Genotype's walls
        self._mutate_walls(self.walls, per_site_mut_rate,
                               mut_effect_size, rand)

    def _mutate_walls(self, walls: list, per_site_mut_rate: float,
                      mut_effect_size: float, rand: random.Random) -> None:
        """
        Mutate WallPair genes.

        A helper function to mutate a Genotype's WallPair genes. Iterates
        through each WallPair object in the list of walls and over each gene
        in each WallPair object.

        :param walls: A list of WallPair objects.
        :type walls: list
        :param per_site_mut_rate: The % chance any given variable in the Genotype will be mutated.
        :type per_site_mut_rate: float
        :param mut_effect_size: The mutation amplitude when a mutation takes place.
        :type mut_effect_size: float
        :param rand: Random number generator object.
        :type rand: random.Random
        :rtype: None
        """
        wallpair_genes = ["angle", "ridge_height", "ridge_width_top",
                          "ridge_width_bottom", "ridge_thickness_top",
                          "ridge_thickness_bottom"]
        # Iterate over each WallPair object in the walls list
        for wp in walls:
            # Iterate over each gene in the WallPair
            for gene in wallpair_genes:
                # if it's randomly selected to mutate, apply a mutation
                    # of mut_effect_size in Guassian distribution
                if per_site_mut_rate >= rand.uniform(0, 1):
                    # angle gene
                    if gene == "angle":
                        wp.angle = wp.angle + rand.gauss(0,mut_effect_size)
                        # if under min bound, set to min
                        wp.angle = max(wp.angle, wp.MIN_ANGLE)
                        # if over max bound, set to max
                        wp.angle = min(wp.angle, wp.MAX_ANGLE)

                    # ridge_height gene
                    if gene == "ridge_height":
                        wp.ridge_height = wp.ridge_height + rand.gauss(0,
                                                                 mut_effect_size)
                        # if under min bound, set to min
                        wp.ridge_height = max(wp.ridge_height, wp.MIN_HEIGHT)
                        # if over max bound, set to max
                        wp.ridge_height = min(wp.ridge_height, wp.MAX_HEIGHT)

                    # ridge_width_top gene
                    if gene == "ridge_width_top":
                        wp.ridge_width_top = (wp.ridge_width_top +
                                              rand.gauss(0,
                                                             mut_effect_size))
                        # if under min bound, set to min
                        wp.ridge_width_top = max(wp.ridge_width_top,
                                                 wp.MIN_RIDGE_WIDTH_TOP)
                        # if over max bound, set to max
                        wp.ridge_width_top = min(wp.ridge_width_top,
                                                 wp.MAX_RIDGE_WIDTH_TOP)

                    # ridge_width_bottom gene
                    if gene == "ridge_width_bottom":
                        wp.ridge_width_bottom = (wp.ridge_width_bottom +
                                                 rand.gauss(0, mut_effect_size))
                        # if under min bound, set to min
                        wp.ridge_width_bottom = max(wp.ridge_width_bottom,
                                                    wp.MIN_RIDGE_WIDTH_BOTTOM)
                        # if over max bound, set to max
                        wp.ridge_width_bottom = min(wp.ridge_width_bottom,
                                                    wp.MAX_RIDGE_WIDTH_BOTTOM)

                    # ridge_thickness_top gene
                    if gene == "ridge_thickness_top":
                        wp.ridge_thickness_top = (wp.ridge_thickness_top +
                                                  rand.gauss(0,
                                                             mut_effect_size))
                        # if under min bound, set to min
                        wp.ridge_thickness_top = max(wp.ridge_thickness_top,
                                                  wp.MIN_RIDGE_THICKNESS_TOP)
                        # if over max bound, set to max
                        wp.ridge_thickness_top = min(wp.ridge_thickness_top,
                                                  wp.MAX_RIDGE_THICKNESS_TOP)

                    # ridge_thickness_bottom gene
                    if gene == "ridge_thickness_bottom":
                        wp.ridge_thickness_bottom = (
                                wp.ridge_thickness_bottom + rand.gauss(0,
                                                                       mut_effect_size))
                        # if under min bound, set to min
                        wp.ridge_thickness_bottom = max(
                            wp.ridge_thickness_bottom, wp.MIN_RIDGE_THICKNESS_BOTTOM)
                        # if over max bound, set to max
                        wp.ridge_width_bottom = min(
                            wp.ridge_thickness_bottom, wp.MAX_RIDGE_THICKNESS_BOTTOM)

    # TODO KATE - func to construct from 2 parents with crossover (not for v1)

    # TODO ALEX - func to write Genotype genes to CSV line
