"""
Helper class for constructing a WallPair and acting upon it.

This module provides:
- generate_without_ridge: randomly generates a WallPair without a ridge.
- generate_with_ridge: randomly generates a WallPair with a ridge.
- generate_list: randomly generates a list of WallPairs.
"""
import random
from typing import Optional

from src.GENETIS_RHINO.parameters import ParametersObject


class WallPair:
    """
    WallPair class.

    This is a helper class representing a wall pair.
    A wall pair is the two walls opposite one another on an antenna.

    :param angle: The angle of the wall pair. Must be between 0 and 90
    degrees. Defaults to None.
    :type angle: float, optional
    :param ridge_height: The flare_height of the ridge as a percent of the horn.
    :type ridge_height: float, optional
    :param ridge_width_top: The width of the ridge as a percent of wall width
    at the top of the horn.
    :type ridge_width_top: float, optional
    :param ridge_width_top: The width of the ridge as a percent of wall width
    at the top of the horn.
    :type ridge_width_top: float, optional
    :param ridge_thickness_top: The thickness of the ridge as a percent of the
    wall width
    :type ridge_thickness_top: float, optional
    """

    def __init__(self, cfg: ParametersObject,
                 angle: Optional[float] = None,
                 ridge_height: Optional[float] = None,
                 ridge_width_top: Optional[float] = None,
                 ridge_width_bottom: Optional[float] = None,
                 ridge_thickness_top: Optional[float] = None,
                 ridge_thickness_bottom: Optional[float] = None) -> None:
        """
        Constructor for a WallPair object.

        Constructs a WallPair object with no ridge.

        :param angle: The angle of the wall pair. Must be between 0 and 90
        degrees. Defaults to None.
        :type angle: float, optional
        :param ridge_height: The flare_height of the ridge as a percentage of the
        total horn flare_height. Starts from bottom of horn. Must be between 0%
        and 100%(inclusive).
        :type ridge_height: float, optional
        :param ridge_width_top: The width of the ridge at the top of the horn.
        Must be between 0 cm and 100 cm (inclusive).
        :type ridge_width_top: float, optional
        :param ridge_width_bottom: The width of the ridge at the bottom of
        the .
        Must be between 0 cm and 100 cm (inclusive).
        :type ridge_width_bottom: float, optional
        :param ridge_thickness_top: The thickness of the ridge. Must be
        between 0 cm
        and 100 cm (inclusive).
        :type ridge_thickness_top: float, optional
        :param ridge_thickness_bottom: The thickness of the ridge at the
        bottom of the . Must be between 0 cm and 100 cm (inclusive).
        :type ridge_thickness_bottom: float, optional
        :rtype: None
        """
        # config
        self.cfg = cfg

        self.NUM_WALL_PAIRS = int(cfg.NUM_WALL_PAIRS)

        # Logical constraint constants
        self.MIN_ANGLE = float(cfg.MIN_ANGLE)  # degrees; exclusive
        self.MAX_ANGLE = float(cfg.MAX_ANGLE)  # degrees; inclusive

        self.MIN_RIDGE_HEIGHT = float(cfg.MIN_RIDGE_HEIGHT)  # % of horn;
        # exclusive
        self.MAX_RIDGE_HEIGHT = float(cfg.MAX_RIDGE_HEIGHT)  # % of horn;
        # inclusive

        self.MIN_RIDGE_WIDTH_TOP = float(cfg.MIN_RIDGE_WIDTH_TOP)  # % of wall
        # width at top of horn; inclusive
        self.MAX_RIDGE_WIDTH_TOP = float(cfg.MAX_RIDGE_WIDTH_TOP) # %;
        # inclusive

        self.MIN_RIDGE_WIDTH_BOTTOM = float(cfg.MIN_RIDGE_WIDTH_BOTTOM)  # %;
        # inclusive
        self.MAX_RIDGE_WIDTH_BOTTOM = float(cfg.MAX_RIDGE_WIDTH_BOTTOM)  # %;
        # inclusive

        self.MIN_RIDGE_THICKNESS_TOP = float(cfg.MIN_RIDGE_THICKNESS_TOP)  # %
        # of distance to the middle of the horn; inclusive
        self.MAX_RIDGE_THICKNESS_TOP = float(cfg.MAX_RIDGE_THICKNESS_TOP)  #%;
        # inclusive

        self.MIN_RIDGE_THICKNESS_BOTTOM = (
            float(cfg.MIN_RIDGE_THICKNESS_BOTTOM))  # %; % of distance to the
            # middle of the horn; inclusive
        self.MAX_RIDGE_THICKNESS_BOTTOM = (
            float(cfg.MAX_RIDGE_THICKNESS_BOTTOM))   # %; inclusive

        # WallPair variables
        self.has_ridge = False
        self.angle = angle
        self.ridge_height = ridge_height
        self.ridge_width_top = ridge_width_top
        self.ridge_width_bottom = ridge_width_bottom
        self.ridge_thickness_top = ridge_thickness_top
        self.ridge_thickness_bottom = ridge_thickness_bottom

    def generate_without_ridge(self, rand: random.Random) -> "WallPair":
        """
        Generates a WallPair without a ridge.

        Generates a random WallPair object with no ridge.

        :param rand: The random number generator.
        :type rand: class:'random.Random'
        :return: A randomly generated WallPair object with no ridge.
        :rtype: WallPair object
        """
        # Generate a random angle within the specified constraints
        angle = rand.uniform(self.MIN_ANGLE, self.MAX_ANGLE)

        # Generate a random ridge_height within the specified constraints
        ridge_height = rand.uniform(self.MIN_RIDGE_HEIGHT,
                                      self.MAX_RIDGE_HEIGHT)

        # Generate a random ridge_width within the specified constraints
        ridge_width_top = rand.uniform(self.MIN_RIDGE_WIDTH_TOP,
                                     self.MAX_RIDGE_WIDTH_TOP)

        ridge_width_bottom = rand.uniform(self.MIN_RIDGE_WIDTH_BOTTOM,
                                       self.MAX_RIDGE_WIDTH_BOTTOM)

        # Generate a random ridge_thickness within the specified constraints
        ridge_thickness_top = rand.uniform(self.MIN_RIDGE_THICKNESS_TOP,
                                         self.MAX_RIDGE_THICKNESS_TOP)

        ridge_thickness_bottom = rand.uniform(self.MIN_RIDGE_THICKNESS_BOTTOM,
                                       self.MAX_RIDGE_THICKNESS_BOTTOM)

        return WallPair(self.cfg, angle, ridge_height, ridge_width_top,
                        ridge_width_bottom,
                        ridge_thickness_top, ridge_thickness_bottom)

    def generate_with_ridge(self, rand: random.Random) -> "WallPair":
        """
        Generates a random WallPair object with a ridge.

        :param rand: The random number generator.
        :type rand: class:'random.Random'
        :return: A randomly generated WallPair object with a ridge.
        :rtype: WallPair object
        """
        # Randomly generate a WallPair object without a ridge
        wp = WallPair(self.cfg).generate_without_ridge(rand)

        # Ensure none of the ridge-defining variables are set to 0
        while wp.ridge_height == 0:
            wp.ridge_height = rand.uniform(self.MIN_RIDGE_HEIGHT,
                                             self.MAX_RIDGE_HEIGHT)

        while wp.ridge_width_top == 0:
            wp.ridge_width_top = rand.uniform(self.MIN_RIDGE_WIDTH_TOP,
                                            self.MAX_RIDGE_WIDTH_TOP)

        while wp.ridge_width_bottom == 0:
            wp.ridge_width_bottom = rand.uniform(
                self.MIN_RIDGE_WIDTH_BOTTOM,
                self.MAX_RIDGE_WIDTH_BOTTOM)

        while wp.ridge_thickness_top == 0:
            wp.ridge_thickness_top = rand.uniform(
                self.MIN_RIDGE_THICKNESS_TOP,
                self.MAX_RIDGE_THICKNESS_TOP)

        while wp.ridge_thickness_bottom == 0:
            wp.ridge_thickness_bottom = rand.uniform(
                self.MIN_RIDGE_THICKNESS_BOTTOM,
                self.MAX_RIDGE_THICKNESS_BOTTOM)

        # Express ridge
        wp.has_ridge = True

        return wp

    def generate_walls_with_ridge(self, rand: random.Random) -> list:
        """
        Generates a list of randomly generated WallPair objects with a ridge.

        :param rand: The random number generator.
        :type rand: class:'random.Random'
        :return: A list of randomly generated WallPair objects.
        :rtype: list[WallPair object]
        """
        # Throw a ValueError if num_wall_pairs is <= 0
        if self.NUM_WALL_PAIRS <= 0:
            raise ValueError("num_wall_pairs must be greater than zero.")

        # Generate random wall pairs and add them to a list
        walls = [WallPair(self.cfg).generate_with_ridge(rand) for _ in
                 range(self.NUM_WALL_PAIRS)]
        return walls

    def generate_walls_without_ridge(self,
                                   rand: random.Random) -> list:
        """
        Generates a list of random WallPair objects without a ridge.

        :param rand: The random number generator.
        :type rand: class:'random.Random'
        :return: A list of randomly generated WallPair objects.
        :rtype: list[WallPair object]
        """
        # Throw a ValueError if num_wall_pairs is <= 0
        if self.NUM_WALL_PAIRS <= 0:
            raise ValueError("num_wall_pairs must be greater than zero.")

        # Generate random wall pairs and add them to a list
        walls = [WallPair(self.cfg).generate_without_ridge(rand) for _ in
                 range(self.NUM_WALL_PAIRS)]
        return walls

    def mutate(self, per_site_mut_rate: float,
                      mut_effect_size: float, rand: random.Random) -> None:
        """
        Mutate WallPair genes.

        A helper function to mutate a WallPair's genes. Iterates
        through each WallPair gene.

        :param per_site_mut_rate: The % chance any given variable in the
        WallPair will be mutated.
        :type per_site_mut_rate: float
        :param mut_effect_size: The mutation amplitude when a mutation takes place.
        :type mut_effect_size: float
        :param rand: Random number generator object.
        :type rand: random.Random
        :rtype: None
        """
        wall_pair_genes = ["angle", "ridge_height", "ridge_width_top",
                          "ridge_width_bottom", "ridge_thickness_top",
                          "ridge_thickness_bottom"]
        # Iterate over each gene in the WallPair
        for gene in wall_pair_genes:
            # if it's randomly selected to mutate, apply a mutation
            # of mut_effect_size in Gaussian distribution
            if per_site_mut_rate >= rand.uniform(0, 1):
                # angle gene
                if gene == "angle":
                    self.angle = self.angle + rand.gauss(0,mut_effect_size)
                    # if under min bound, set to min
                    self.angle = max(self.angle, self.MIN_ANGLE)
                    # if over max bound, set to max
                    self.angle = min(self.angle, self.MAX_ANGLE)

                # ridge_height gene
                if gene == "ridge_height":
                    self.ridge_height = self.ridge_height + rand.gauss(0,
                                                                   mut_effect_size)
                    # if under min bound, set to min
                    self.ridge_height = max(self.ridge_height,
                                          self.MIN_RIDGE_HEIGHT)
                    # if over max bound, set to max
                    self.ridge_height = min(self.ridge_height,
                                          self.MAX_RIDGE_HEIGHT)

                # ridge_width_top gene
                if gene == "ridge_width_top":
                    self.ridge_width_top = (self.ridge_width_top +
                                          rand.gauss(0,
                                                     mut_effect_size))
                    # if under min bound, set to min
                    self.ridge_width_top = max(self.ridge_width_top,
                                             self.MIN_RIDGE_WIDTH_TOP)
                    # if over max bound, set to max
                    self.ridge_width_top = min(self.ridge_width_top,
                                             self.MAX_RIDGE_WIDTH_TOP)

                # ridge_width_bottom gene
                if gene == "ridge_width_bottom":
                    self.ridge_width_bottom = (self.ridge_width_bottom +
                                             rand.gauss(0, mut_effect_size))
                    # if under min bound, set to min
                    self.ridge_width_bottom = max(self.ridge_width_bottom,
                                                self.MIN_RIDGE_WIDTH_BOTTOM)
                    # if over max bound, set to max
                    self.ridge_width_bottom = min(self.ridge_width_bottom,
                                                self.MAX_RIDGE_WIDTH_BOTTOM)

                # ridge_thickness_top gene
                if gene == "ridge_thickness_top":
                    self.ridge_thickness_top = (self.ridge_thickness_top +
                                              rand.gauss(0,
                                                         mut_effect_size))
                    # if under min bound, set to min
                    self.ridge_thickness_top = max(self.ridge_thickness_top,
                                                 self.MIN_RIDGE_THICKNESS_TOP)
                    # if over max bound, set to max
                    self.ridge_thickness_top = min(self.ridge_thickness_top,
                                                 self.MAX_RIDGE_THICKNESS_TOP)

                # ridge_thickness_bottom gene
                if gene == "ridge_thickness_bottom":
                    self.ridge_thickness_bottom = (self.ridge_thickness_bottom +
                                                   rand.gauss(0,
                                                              mut_effect_size))
                    # if under min bound, set to min
                    self.ridge_thickness_bottom = max(
                        self.ridge_thickness_bottom,
                        self.MIN_RIDGE_THICKNESS_BOTTOM)
                    # if over max bound, set to max
                    self.ridge_width_bottom = min(
                        self.ridge_thickness_bottom,
                        self.MAX_RIDGE_THICKNESS_BOTTOM)
