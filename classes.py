#Python imports
from bdb import effective
from math import pi, sqrt
from turtle import width


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


class Concrete:

    def __init__(self, fc = 28, eu = 0.003, EC_factor = 3900):
        self.fc = fc
        self.eu = eu
        self.EC = EC_factor*sqrt(self.fc)


class Steel:

    def __init__(self, fy = 420, ES = 200000):
        self.fy = fy
        self.ES = ES
   

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

    def __init__(self, geometry, cover, concrete, steel, reinforcement):
        self.width = geometry.lenght_1
        self.height = geometry.lenght_2
        self.cover = cover
        self.fc = concrete.fc
        self.fy = steel.fy
        self.rebar = reinforcement
    

    #Region Methods
       
    def effective_height(self, reinforcement_diameter):
        effective_height = self.height- self.cover - self.rebar.stirrup_rebar_diameter - reinforcement_diameter/2
        return effective_height
    
    def flexural_ro(self, rebar_area, effective_height):
        flexural_ro = rebar_area/(self.width*effective_height)
        return flexural_ro

    def simple_nominal_moment_strenght(self, flexural_ro, effective_height):
        nominal_moment = 0.9*self.fy*flexural_ro*self.width*effective_height**2*(1-0.59*flexural_ro*self.fc/self.fy)*1000
        return nominal_moment
    
    #Region Properties

    @property
    def top_effective_height(self):
        top_effective_height = self.effective_height(self.rebar.top_rebar_diameter)
        return top_effective_height
    
    @property
    def top_flexural_ro(self):
        top_flexural_ro = self.flexural_ro(self.rebar.top_total_rebar_area, self.top_effective_height)
        return top_flexural_ro
    
    @property
    def simple_top_nominal_moment_strenght(self):
        simple_top_nominal_moment_strenght = self.simple_nominal_moment_strenght(self.top_flexural_ro, self.top_effective_height)
        return simple_top_nominal_moment_strenght


    
        

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


