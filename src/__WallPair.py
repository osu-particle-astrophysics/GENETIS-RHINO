class __WallPair:
    """
       A class representing a wall pair.

       Attributes:
           width (float): The width of the wall pair.
           angle (float): The angle of the wall pair.
           has_ridge (bool): True if the wall pair has a ridge.
           ridge_width (float): The width of the ridge.
           ridge_height (float): The height of the ridge.
           ridge_thickness (float): The thickness of the ridge.
       """

    def __init__(self, width, angle, has_ridge, ridge_width, ridge_height, ridge_thickness):
        """
            Initializes a WallPair object.

               Parameters:
                   width (float): The width of the wall pair.
                   angle (float): The angle of the wall pair. Must be between 0 and 90.
                   has_ridge (bool): True if the wall pair has a ridge.
                   ridge_width (float): The width of the ridge.
                   ridge_height (float): The height of the ridge.
                   ridge_thickness (float): The thickness of the ridge.
               """

        self.width = width
        self.angle = angle
        self.has_ridge = has_ridge
        self.ridge_width = ridge_width
        self.ridge_height = ridge_height
        self.ridge_thickness = ridge_thickness



