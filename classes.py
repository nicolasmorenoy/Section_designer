
from turtle import width


class RectangularGeometry:
    """
    Class with all the geometry asspects of the element, including lenght of span; base, height
    """

    def __init__(self, width, height, lenght):
        self.widht = width
        self.height = height
        self.lenght = lenght


class Materials:
    """
    Class with all the information about the materials to be used in the element.
    """

    def __init__(self, fc, fy, EC, ES):
        self.fc = fc
        self.fy = fy
        self.EC = EC
        self.ES = ES


class Beam:
    """
    Class that contains all the information about a created beam

    """

    def __init__(self, geometry, materials, reinforcement):
        pass

