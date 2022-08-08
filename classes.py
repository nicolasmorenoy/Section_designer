from math import pi


# class RectangularGeometry:
#     """
#     Class with all the geometry asspects of the element, including lenght of span; base, height
#     """

#     def __init__(self, width, height, lenght):
#         self.widht = width
#         self.height = height
#         self.lenght = lenght


# class Materials:
#     """
#     Class with all the information about the materials to be used in the element.
#     """

#     def __init__(self, fc, fy, EC, ES):
#         self.fc = fc
#         self.fy = fy
#         self.EC = EC
#         self.ES = ES


# class Geometry:
#     """
#     Superclass to define the geometrical properties of a structural element.
#     """

#     def __init__(self):
#         pass


class Reinforcement:
    """
    Class that contains all the reinforcement properties
    """

    def __init__(self, top_bars, bottom_bars, top_diameter, bottom_diameter, stirrup_diameter, stirrup_legs):
        self.top_bars = top_bars
        self.bottom_bars = bottom_bars
        self.top_diameter = top_diameter
        self.bottom_diameter = bottom_diameter
        self.stirrup_diameter = stirrup_diameter
        self.stirrup_legs = stirrup_legs

class Beam:
    """
    Class that contains all the information about a created beam

    """

    def __init__(self, width, height, cover, fc, fy, reinforcement):
        self.width = width
        self.height = height
        self.cover = cover
        self.fc = fc
        self.fy = fy
        self.reinforcement = reinforcement
        


    #Properties

    #Reinforcement
    @property
    def reinforcement_properties(self):
        top_diameter = self.reinforcement.top_diameter/8*.0254
        top_area = top_diameter**2*pi/4

        return top_diameter, top_area




if __name__ == '__main__':
    print("This is not the script you should be executing")

