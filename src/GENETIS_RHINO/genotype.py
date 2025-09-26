"""
Class for constructing an antenna Genotype and acting upon it.

This module provides:
- generate: randomly generates a new Genotype
- mutate: mutates the Genotype
"""
import random
from typing import Optional

from src.GENETIS_RHINO.parameters import ParametersObject
from src.GENETIS_RHINO.wall_pair import WallPair


class Genotype:
    """Genotype class."""

    def __init__(self, cfg: ParametersObject,
                 flare_length: Optional[float] = None,
                 waveguide_height: Optional[float] = None,
                 waveguide_length: Optional[float] = None,
                 waveguide_width: Optional[float] = None,
                 walls: Optional[list] = None) -> None:
        """
        Genotype Constructor.

        The constructor for a Genotype object (an individual antenna's
        genotype).

        :param cfg: The parameters of the antenna
        :type cfg: ParametersObject
        :param flare_length: The length of the antenna's flare
        :type flare_length: float, optional
        :param waveguide_height: The flare_height of the waveguide.
        :type waveguide_height: float, optional
        :param waveguide_length: The length of the waveguide.
        :type waveguide_length: float, optional
        :param waveguide_width: The length of the waveguide.
        :type waveguide_width: float, optional
        :param walls: A list of WallPair objects that comprise the walls of the
        antenna.
        :type walls: list, optional
        :rtype: None
        """
        self.cfg = cfg

        self.NUM_WALL_PAIRS = cfg.NUM_WALL_PAIRS

        # Logical constraint constants
        self.MIN_FLARE_LENGTH = float(cfg.MIN_FLARE_LENGTH)
        self.MAX_FLARE_LENGTH = float(cfg.MAX_FLARE_LENGTH)

        # cm; inclusive
        self.MIN_WAVEGUIDE_LENGTH = float(cfg.MIN_WAVEGUIDE_LENGTH)
        self.MAX_WAVEGUIDE_LENGTH = float(cfg.MAX_WAVEGUIDE_LENGTH)

        self.MIN_WAVEGUIDE_HEIGHT = float(cfg.MIN_WAVEGUIDE_HEIGHT) # cm;
        # inclusive -- func of min freq you care about picking up
        self.MAX_WAVEGUIDE_HEIGHT = float(cfg.MAX_WAVEGUIDE_HEIGHT) # cm;
        # inclusive; # TODO also prevent being bigger than aperture smaller area
        # rectangle than waveguide

        self.MIN_WAVEGUIDE_WIDTH = float(cfg.MIN_WAVEGUIDE_WIDTH)
        self.MAX_WAVEGUIDE_WIDTH = float(cfg.MAX_WAVEGUIDE_WIDTH)

        # Make sure the list of walls provided to the constructor is valid.
        if walls is not None and not all(isinstance(wall_pair, WallPair) for wall_pair in walls):
            raise ValueError("walls must be a list of WallPair objects.")

        self.flare_length = flare_length
        self.waveguide_height = waveguide_height
        self.waveguide_length = waveguide_length
        self.waveguide_width = waveguide_width
        self.walls = walls

    def generate_with_ridge(self, rand: random.Random) -> "Genotype":
        """
        Generate random Genotype with ridge.

        Makes a Genotype object with randomly generated genes and ridge.

        :param rand: Random number generator object.
        :type rand: random.Random
        :return: Genotype object
        :rtype: Genotype
        """
        # generate valid random flare_length
        flare_length = rand.uniform(self.MIN_FLARE_LENGTH,
                                    self.MAX_FLARE_LENGTH)


        # generate valid random waveguide_height
        waveguide_height = rand.uniform(self.MIN_WAVEGUIDE_HEIGHT,
                                         self.MAX_WAVEGUIDE_HEIGHT)

        # generate valid random waveguide_length
        waveguide_length = rand.uniform(self.MIN_WAVEGUIDE_LENGTH,
                                         self.MAX_WAVEGUIDE_LENGTH)

        # generate valid random waveguide_width
        waveguide_width = rand.uniform(self.MIN_WAVEGUIDE_WIDTH,
                                       self.MAX_WAVEGUIDE_WIDTH)

        # generate list of walls with randomly generated values
        walls = WallPair(self.cfg).generate_walls_with_ridge(rand)

        return Genotype(self.cfg, flare_length, waveguide_height,
                        waveguide_length, waveguide_width, walls)

    def generate_without_ridge(self, rand: random.Random) -> "Genotype":
        """
        Generate random Genotype with ridge.

        Makes a Genotype object with randomly generated genes and ridge.

        :param rand: Random number generator object.
        :type rand: random.Random
        :return: Genotype object
        :rtype: Genotype
        """
        # generate valid random flare_length
        flare_length = rand.uniform(self.MIN_FLARE_LENGTH,
                                    self.MAX_FLARE_LENGTH)


        # generate valid random waveguide_height
        waveguide_height = rand.uniform(self.MIN_WAVEGUIDE_HEIGHT,
                                         self.MAX_WAVEGUIDE_HEIGHT)

        # generate valid random waveguide_length
        waveguide_length = rand.uniform(self.MIN_WAVEGUIDE_LENGTH,
                                         self.MAX_WAVEGUIDE_LENGTH)

        # generate valid random waveguide_width
        waveguide_width = rand.uniform(self.MIN_WAVEGUIDE_WIDTH,
                                       self.MAX_WAVEGUIDE_WIDTH)

        # generate list of walls with randomly generated values
        walls = WallPair(self.cfg).generate_walls_without_ridge(rand)

        return Genotype(self.cfg, flare_length, waveguide_height,
                        waveguide_length, waveguide_width, walls)

    def mutate(self, rand: random.Random) -> None:
        """
        Mutate Genotype.

        Mutates a genotype.

        :param rand: Random number generator object.
        :type rand: random.Random
        :rtype: None
        """
        per_site_mut_rate = float(self.cfg.per_site_mut_rate)
        mut_effect_size = float(self.cfg.mut_effect_size)

        core_genes = ["flare_length", "waveguide_height", "waveguide_length",
                      "waveguide_width"]

        # Iterate over each gene in the Genotype
        for gene in core_genes:
            # if it's randomly selected to mutate, apply a mutation of
            # mut_effect_size in Gaussian distribution
            if per_site_mut_rate >= rand.uniform(0, 1):
                # flare_length gene
                if gene == "flare_length":
                    self.flare_length = self.flare_length + rand.gauss(0,
                                                                  mut_effect_size)
                    # if under min bound, set to min
                    self.flare_length = max(self.flare_length, self.MIN_FLARE_LENGTH)
                    # if over max bound, set to max
                    self.flare_length = min(self.flare_length, self.MAX_FLARE_LENGTH)

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
                    # if over max bound, set to max
                    self.waveguide_length = min(self.waveguide_length, self.MAX_WAVEGUIDE_LENGTH)

                # waveguide_width gene
                elif gene == "waveguide_width":
                    self.waveguide_width = (self.waveguide_width +
                                            rand.gauss(0, mut_effect_size))
                    # if under min bound, set to min
                    self.waveguide_width = max(self.waveguide_width, self.MIN_WAVEGUIDE_WIDTH)
                    # if over max bound, set to max
                    self.waveguide_width = min(self.waveguide_width, self.MAX_WAVEGUIDE_WIDTH)

        # mutate the Genotype's walls
        for wp in self.walls:
            wp.mutate(per_site_mut_rate, mut_effect_size, rand)

    # TODO KATE - func to construct from 2 parents with crossover (not for v1)
