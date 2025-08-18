"""
Class for constructing a WallPair and acting upon it.

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
    A wall pair is the two sides of one sheet of material used to make an
    antenna wall.

    :param has_ridge: Whether the wall pair has a ridge or not. Can only be
    true if all ridge variables are greater than 0. Defaults to None.
    :type has_ridge: bool, optional
    :param width: The width of the wall pair. Must be > 0 cm and <= 100 cm.
    Defaults to None.
    :type width: float, optional
    :param angle: The angle of the wall pair. Must be between 0 and 90
    degrees (inclusive). Defaults to None.
    :type angle: float, optional
    :param ridge_height: The height of the ridge. Must be between 0 cm and
    100 cm (inclusive).
    :type ridge_height: float, optional
    :param ridge_width: The width of the ridge. Must be between 0 cm and
    100 cm (inclusive).
    :type ridge_width: float, optional
    :param ridge_thickness: The thickness of the ridge. Must be between 0 cm
    and 100 cm (inclusive).
    :type ridge_thickness: float, optional
    """

    # Logical constraint constants  #TODO set to correct units and values
    MIN_WIDTH = 0.0             # cm; exclusive
    MAX_WIDTH = 100.0           # cm; inclusive

    MIN_ANGLE = 0.0             # degrees; exclusive
    MAX_ANGLE = 100.0           # degrees; inclusive

    MIN_RIDGE_HEIGHT = 0.0      # cm; inclusive
    MAX_RIDGE_HEIGHT = 100.0    # cm; inclusive

    MIN_RIDGE_WIDTH = 0.0       # cm; inclusive
    MAX_RIDGE_WIDTH = 100.0     # cm; inclusive

    MIN_RIDGE_THICKNESS = 0.0   # cm; inclusive
    MAX_RIDGE_THICKNESS = 100.0 # cm; inclusive

    def __init__(self, has_ridge: Optional[bool] = None,
                 width: Optional[float] = None,
                 angle: Optional[float] = None,
                 ridge_height: Optional[float] = None,
                 ridge_width: Optional[float] = None,
                 ridge_thickness: Optional[float] = None) -> None:
        """Constructor method."""
        # If has_ridge is True, make sure all ridge variables are greater
        # than 0.
        if has_ridge and (ridge_height <= 0 or ridge_width <= 0 or ridge_thickness <= 0):
            raise ValueError("WallPair has_ridge can only be True if all ridge variables are greater than 0.")

        self.has_ridge = has_ridge
        self.width = width
        self.angle = angle
        self.ridge_height = ridge_height
        self.ridge_width = ridge_width
        self.ridge_thickness = ridge_thickness

    def generate_without_ridge(self, rand: random.Random) -> object:
        """
        Generates a WallPair without a ridge.

        Generates a random WallPair object with no ridge.

        :param rand: The random number generator.
        :type rand: class:'random.Random'
        :return: A randomly generated WallPair object with no ridge.
        :rtype: WallPair object
        """
        # Do not express ridge
        has_ridge = False

        # Generate a random width within the specified constraints
        width = WallPair.MIN_WIDTH
        while width == WallPair.MIN_WIDTH:  # exclude min
            width = rand.uniform(WallPair.MIN_WIDTH, WallPair.MAX_WIDTH)

        # Generate a random angle within the specified constraints
        angle = rand.uniform(WallPair.MIN_ANGLE, WallPair.MAX_ANGLE)

        # Generate a random ridge_height within the specified constraints
        ridge_height = rand.uniform(WallPair.MIN_RIDGE_HEIGHT,
                                      WallPair.MAX_RIDGE_HEIGHT)

        # Generate a random ridge_width within the specified constraints
        ridge_width = rand.uniform(WallPair.MIN_RIDGE_WIDTH,
                                     WallPair.MAX_RIDGE_WIDTH)

        # Generate a random ridge_thickness within the specified constraints
        ridge_thickness = rand.uniform(WallPair.MIN_RIDGE_THICKNESS,
                                         WallPair.MAX_RIDGE_THICKNESS)

        return WallPair(has_ridge, width, angle, ridge_height, ridge_width,
                        ridge_thickness)

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

        while wp.ridge_width == 0:
            wp.ridge_width = rand.uniform(WallPair.MIN_RIDGE_WIDTH,
                                            WallPair.MAX_RIDGE_WIDTH)

        while wp.ridge_thickness == 0:
            wp.ridge_thickness = rand.uniform(WallPair.MIN_RIDGE_THICKNESS,
                                                WallPair.MAX_RIDGE_THICKNESS)

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
