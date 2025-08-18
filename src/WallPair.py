"""
Helper class for constructing a WallPair and acting upon it.

This module provides:
- generate_without_ridge: randomly generates a WallPair without a ridge.
- generate_with_ridge: randomly generates a WallPair with a ridge.
- generate_list: randomly generates a list of WallPairs.
"""
import random
from typing import Optional


class WallPair:
    """
    WallPair class.

    This is a helper class representing a wall pair.
    A wall pair is the two walls opposite one another on an antenna.

    :param has_ridge: Whether the wall pair has a ridge or not. Can only be
    true if all ridge variables are greater than 0. Initialized as False.
    :type has_ridge: bool, optional
    :param angle: The angle of the wall pair. Must be between 0 and 90
    degrees. Defaults to None.
    :type angle: float, optional
    :param ridge_height: The height of the ridge as a percent of the horn.
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

    # Logical constraint constants
    MIN_ANGLE = 0.0              # degrees; exclusive
    MAX_ANGLE = 90.0             # degrees; inclusive

    MIN_RIDGE_HEIGHT = 0.0       # % of horn; exclusive
    MAX_RIDGE_HEIGHT = 100.0     # % of horn; inclusive

    MIN_RIDGE_WIDTH_TOP = 0.0    # % of wall width at top of horn; inclusive
    MAX_RIDGE_WIDTH_TOP = 100.0  # %; inclusive

    MIN_RIDGE_WIDTH_BOTTOM = 0.0     # %; inclusive
    MAX_RIDGE_WIDTH_BOTTOM = 100.0   # %; inclusive

    MIN_RIDGE_THICKNESS_TOP = 0.0    # % of distance to the middle of the
    # horn; inclusive
    MAX_RIDGE_THICKNESS_TOP = 100.0  # %; inclusive

    MIN_RIDGE_THICKNESS_BOTTOM = 0.0    # %; % of distance to the middle of
    # the horn; inclusive
    MAX_RIDGE_THICKNESS_BOTTOM = 100.0  # %; inclusive

    def __init__(self, angle: Optional[float] = None,
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
        :param ridge_height: The height of the ridge as a percentage of the
        total horn height. Starts from bottom of horn. Must be between 0%
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
        """
        self.has_ridge = False
        self.angle = angle
        self.ridge_height = ridge_height
        self.ridge_width_top = ridge_width_top
        self.ridge_width_bottom = ridge_width_bottom
        self.ridge_thickness_top = ridge_thickness_top
        self.ridge_thickness_bottom = ridge_thickness_bottom

    def generate_without_ridge(self, rand: random.Random) -> object:
        """
        Generates a WallPair without a ridge.

        Generates a random WallPair object with no ridge.

        :param rand: The random number generator.
        :type rand: class:'random.Random'
        :return: A randomly generated WallPair object with no ridge.
        :rtype: WallPair object
        """
        # Generate a random angle within the specified constraints
        angle = rand.uniform(WallPair.MIN_ANGLE, WallPair.MAX_ANGLE)

        # Generate a random ridge_height within the specified constraints
        ridge_height = rand.uniform(WallPair.MIN_RIDGE_HEIGHT,
                                      WallPair.MAX_RIDGE_HEIGHT)

        # Generate a random ridge_width within the specified constraints
        ridge_width_top = rand.uniform(WallPair.MIN_RIDGE_WIDTH_TOP,
                                     WallPair.MAX_RIDGE_WIDTH_TOP)

        ridge_width_bottom = rand.uniform(WallPair.MIN_RIDGE_WIDTH_BOTTOM,
                                       WallPair.MAX_RIDGE_WIDTH_BOTTOM)

        # Generate a random ridge_thickness within the specified constraints
        ridge_thickness_top = rand.uniform(WallPair.MIN_RIDGE_THICKNESS_TOP,
                                         WallPair.MAX_RIDGE_THICKNESS_TOP)

        ridge_thickness_bottom = rand.uniform(
            WallPair.MIN_RIDGE_THICKNESS_BOTTOM,
                                       WallPair.MAX_RIDGE_THICKNESS_BOTTOM)

        return WallPair(angle, ridge_height, ridge_width_top, ridge_width_bottom,
                        ridge_thickness_top, ridge_thickness_bottom)

    def generate_with_ridge(self, rand: random.Random) -> object:
        """
        Generates a random WallPair object with a ridge.

        :param rand: The random number generator.
        :type rand: class:'random.Random'
        :return: A randomly generated WallPair object with a ridge.
        :rtype: WallPair object
        """
        # Randomly generate a WallPair object without a ridge
        wp = WallPair().generate_without_ridge(rand)

        # Ensure none of the ridge-defining variables are set to 0
        while wp.ridge_height == 0:
            wp.ridge_height = rand.uniform(WallPair.MIN_RIDGE_HEIGHT,
                                             WallPair.MAX_RIDGE_HEIGHT)

        while wp.ridge_width_top == 0:
            wp.ridge_width_top = rand.uniform(WallPair.MIN_RIDGE_WIDTH_TOP,
                                            WallPair.MAX_RIDGE_WIDTH_TOP)

        while wp.ridge_width_bottom == 0:
            wp.ridge_width_bottom = rand.uniform(
                WallPair.MIN_RIDGE_WIDTH_BOTTOM,
                WallPair.MAX_RIDGE_WIDTH_BOTTOM)

        while wp.ridge_thickness_top == 0:
            wp.ridge_thickness_top = rand.uniform(
                WallPair.MIN_RIDGE_THICKNESS_TOP,
                WallPair.MAX_RIDGE_THICKNESS_TOP)

        while wp.ridge_thickness_bottom == 0:
            wp.ridge_thickness_bottom = rand.uniform(
                WallPair.MIN_RIDGE_THICKNESS_BOTTOM,
                WallPair.MAX_RIDGE_THICKNESS_BOTTOM)

        # Express ridge
        wp.has_ridge = True

        return wp

    def generate_list(self, num_wall_pairs: int, rand: random.Random) -> list:
        """
        Generates a list of randomly generated WallPair objects.

        :param num_wall_pairs: The number of wall pairs to generate. Must be greater than zero.
        :type num_wall_pairs: int
        :param rand: The random number generator.
        :type rand: class:'random.Random'
        :return: A list of randomly generated WallPair objects.
        :rtype: list[WallPair object]
        """
        # Throw a ValueError if num_wall_pairs is <= 0
        if num_wall_pairs <= 0:
            raise ValueError("num_wall_pairs must be greater than zero.")

        # Generate random wall pairs and add them to a list
        walls = []
        for _ in range(num_wall_pairs):
            # Randomly select type of wall pair to generate (ridge or no ridge)
            if random.randint(0,1) == 0:  #TODO do we actually want these to
                # be equal odds?
                walls.append(WallPair().generate_without_ridge(rand))
            else:
                walls.append(WallPair().generate_with_ridge(rand))
        return walls
