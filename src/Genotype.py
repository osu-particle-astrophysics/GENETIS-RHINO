class Genotype:
    """
       A class representing an individual antenna's genotype.

       Attributes:

           num_wall_pairs (int): The # of wall-pairs of an individual horn antenna.
           walls[__WallPair]: A list of WallPair objects.
           height (float): The height of the antenna.
           waveguide_length (float): The length of the waveguide.
           waveguide_height (float): The height of the waveguide.
       """


    def __init__(self, num_wall_pairs, height, waveguide_length, waveguide_height):
        """
            Initializes a Genotype object.

                Parameters:
                    num_wall_pairs (int): The # of wall-pairs of an individual horn antenna.
                    walls[__WallPair]: A list of WallPair objects.
                    height (float): The height of the antenna.
                    waveguide_length (float): The length of the waveguide.
                    waveguide_height (float): The height of the waveguide.
                """
        self.num_wall_pairs = num_wall_pairs
        self.height = height
        self.waveguide_length = waveguide_length
        self.waveguide_height = waveguide_height