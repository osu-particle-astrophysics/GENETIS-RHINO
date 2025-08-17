import random
from src.WallPair import WallPair
import sys


class Genotype:
    """
    A class representing an individual antenna's genotype.

    Attributes:

        height (float): The height of the antenna.
        waveguide_height (float): The height of the waveguide.
        waveguide_length (float): The length of the waveguide.
        walls[WallPair]: A list of WallPair objects that make up the walls of the antenna.
    """

    MIN_HEIGHT = 0.0              # cm; exclusive
    MAX_HEIGHT = 0.0              # cm; inclusive

    MIN_WAVEGUIDE_HEIGHT = 0.0    # cm; exclusive
    MAX_WAVEGUIDE_HEIGHT = 100.0  # cm; inclusive

    MIN_WAVEGUIDE_LENGTH = 0.0    # cm; exclusive
    MAX_WAVEGUIDE_LENGTH = 100.0  # cm; inclusive

    def __init__(self, height=None, waveguide_height=None, waveguide_length=None, walls=None):
        """
        The constructor for a Genotype object (an individual antenna's genotype).

        Parameters:
            height (float): The height of the antenna.
            waveguide_length (float): The length of the waveguide.
            waveguide_height (float): The height of the waveguide.
            walls[WallPair] (list of WallPair objects): A list of WallPair objects that make up the walls of the antenna.
                                                        The list must be exactly 8 WallPair objects to be valid.  # FIXME is this what we want??
        """
        # Make sure the list of walls provided to the constructor is valid. Exit program if invalid.
        if not all(isinstance(item, WallPair) for item in walls):
             raise ValueError("List must contain exactly 8 WallPair objects.")

        self.height = height
        self.waveguide_height = waveguide_height
        self.waveguide_length = waveguide_length
        self.walls = walls


    def mutate(self, seed, per_site_mut_rate, mut_effect_size):  # FIXME applitude term? need seed here?
        """
         A method to mutate an individual antenna's genotype.
        :param per_site_mut_rate: The % chance any given variable in the Genotype will be mutated.
        :param mut_effect_size: The mutation amplitude when a mutation takes place.
        """
        random.seed(seed)

        core_genes = ["height", "waveguide_height", "waveguide_length"]
        for gene in core_genes:
            if per_site_mut_rate >= random.uniform(0, 1):
                if gene == "height":
                    self.height = self.height + random.gauss(0, mut_effect_size)

                elif gene == "waveguide_height":
                    self.waveguide_height = (self.waveguide_height +
                                            random.gauss(0, mut_effect_size))

                elif gene == "waveguide_length":

                    self.waveguide_length = (self.waveguide_length +
                                            random.gauss(0, mut_effect_size))

                else:
                    sys.exit(1)
        # TODO add WallPair mutating to mutate func


    # TODO func to generate random one
    def generate_random(self, seed, num_walls):

        random.seed(seed)

        # generate valid random height
        height = Genotype.MIN_HEIGHT
        while height == Genotype.MIN_HEIGHT:
            height = random.uniform(Genotype.MIN_HEIGHT, Genotype.MAX_HEIGHT)

        # generate valid random waveguide_height
        waveguide_height = Genotype.MIN_WAVEGUIDE_HEIGHT
        while waveguide_height == Genotype.MIN_WAVEGUIDE_HEIGHT:
            waveguide_height = random.uniform(Genotype.MIN_WAVEGUIDE_HEIGHT, Genotype.MAX_WAVEGUIDE_HEIGHT)

        # generate valid random waveguide_length
        waveguide_length = Genotype.MIN_WAVEGUIDE_LENGTH
        while waveguide_length == Genotype.MIN_WAVEGUIDE_LENGTH:
            waveguide_length = random.uniform(Genotype.MIN_WAVEGUIDE_LENGTH, Genotype.MAX_WAVEGUIDE_LENGTH)

        # generate list of walls
        walls = WallPair.generate_random_list(num_walls, seed)
        return



    # TODO func to construct one from 1 parent

    # TODO func to construct from 2 parents with crossover -- do later

    # TODO func to mutate - each variable has small chance of mutating -

    # TODO write to CSV line

    def print(g):
        print()
        print("Height: " + str(g.height))
        print("Waveguide Height: " + str(g.waveguide_height))
        print("Waveguide Length: " + str(g.waveguide_length))