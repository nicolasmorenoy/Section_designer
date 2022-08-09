#Python imports
from math import pi


class Rectangular:

    def __init__(self, lenght_1, lenght_2, lenght_3):
        self.lenght_1 = lenght_1
        self.lenght_2 = lenght_2
        self.lenght_3 = lenght_3
    

    @property
    def area_1_2(self):
        area_1_2 = self.lenght_1 * self.lenght_2
        return area_1_2
    
    @property
    def area_1_3(self):
        area_1_3 = self.lenght_1 * self.lenght_3
        return area_1_3
    
    @property
    def area_3_2(self):
        area_3_2 = self.lenght_3 * self.lenght_2
        return area_3_2
    
    @property
    def volumen(self):
        volumen = self.lenght_1 * self.lenght_2 * self.lenght_3
        return volumen

class RebarProperties:
    """
    Class that contains the basic reinforcement properties
    """

    def __init__(self, bar_number):
        self.bar_number = bar_number
    
    @property
    def diameter(self):
        diameter = self.bar_number/8*.0254
        return diameter

    @property
    def area(self):
        area = self.diameter**2*pi/4
        return area

class ReinforcementProperties:
    """
    Class that contains all the reinforcement properties
    """

    def __init__(self, top_rebars, bottom_rebars, top_rebar_number, bottom_rebar_number, stirrup_rebar_number, stirrup_legs):
        self.top_bars = top_rebars
        self.bottom_bars = bottom_rebars
        self.top_rebar_diameter = top_rebar_number.diameter
        self.top_rebar_area = top_rebar_number.area
        self.bottom_diameter = bottom_rebar_number.diameter
        self.bottom_rebar_area = bottom_rebar_number.area
        self.stirrup_rebar_diameter = stirrup_rebar_number.diameter
        self.stirrup_rebar_area = stirrup_rebar_number.area
        self.stirrup_legs = stirrup_legs
    

    #Reinforcement properties

    
    @property
    def top_total_rebar_area(self):
        top_total_rebar_area = self.top_rebar_area * self.top_bars
        return top_total_rebar_area

    @property
    def bottom_total_rebar_area(self):
        bottom_total_rebar_area = self.bottom_rebar_area * self.bottom_bars
        return bottom_total_rebar_area
    

class Beam:
    """
    Class that contains all the information about a created beam

    """

    def __init__(self, geometry, cover, fc, fy, reinforcement):
        self.width = geometry.lenght_1
        self.height = geometry.lenght_2
        self.cover = cover
        self.fc = fc
        self.fy = fy
        self.rebar = reinforcement
        

if __name__ == '__main__':
    print("This is not the script you should be executing")




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


