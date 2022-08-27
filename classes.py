#Python imports
from math import pi, sqrt


#Geometry Section
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


class Circular:

    def __init__(self, diameter):
        self.diameter = diameter
        self.area = self.diameter**2*pi/4

    # def get_area(self, diameter = self.diameter):
    #     area = diameter**2*pi/4
    #     return area


#Region Materials
class Concrete:

    def __init__(self, fc = 28, eu = 0.003):
        self.fc = fc
        self.eu = eu
    
    
    @property
    def elastic_modulus(self, EC_factor = 3900):
        elastic_modulus = EC_factor*sqrt(self.fc)
        return elastic_modulus

class Steel:

    def __init__(self, fy = 420, ES = 200000):
        self.fy = fy
        self.ES = ES
   

#Reinforcement
class Rebar:
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
        area = Circular(self.diameter).area
        return area


class ReinforcementProperties:
    """
    Class that contains all the reinforcement properties
    """

    def __init__(self, top_rebars, bottom_rebars, top_rebar_number, bottom_rebar_number, stirrup_legs = 2, stirrup_rebar_number = Rebar(3)):
        self.top_bars = top_rebars
        self.bottom_bars = bottom_rebars
        self.top_rebar_diameter = top_rebar_number.diameter
        self.top_rebar_area = top_rebar_number.area
        self.bottom_rebar_diameter = bottom_rebar_number.diameter
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
            

#Section designer region
class Beam:
    """
    Class that contains all the information about a created beam

    """

    def __init__(self, geometry, cover, concrete, steel, reinforcement, stirrup_spacing = 0.2):
        self.width = geometry.lenght_1
        self.height = geometry.lenght_2
        self.cover = cover
        self.fc = concrete.fc
        self.fy = steel.fy
        self.stirrup_spacing = stirrup_spacing
        self.top_bars = reinforcement.top_bars
        self.bottom_bars = reinforcement.bottom_bars
        self.top_rebar_diameter = reinforcement.top_rebar_diameter
        self.top_rebar_area = reinforcement.top_rebar_area
        self.bottom_rebar_diameter = reinforcement.bottom_rebar_diameter
        self.bottom_rebar_area = reinforcement.bottom_rebar_area
        self.stirrup_rebar_diameter = reinforcement.stirrup_rebar_diameter
        self.stirrup_rebar_area = reinforcement.stirrup_rebar_area
        self.stirrup_legs = reinforcement.stirrup_legs
        self.top_total_rebar_area = reinforcement.top_total_rebar_area
        self.bottom_total_rebar_area = reinforcement.bottom_total_rebar_area
    

    #Region Methods
    #Get Properties Methods
       
    def get_effective_height(self, reinforcement_diameter):
        effective_height = self.height - self.cover - self.stirrup_rebar_diameter - reinforcement_diameter/2
        return effective_height
    
    def get_flexural_ro(self, rebar_area, effective_height):
        flexural_ro = rebar_area/(self.width*effective_height)
        return flexural_ro

    def get_simple_nominal_moment_strenght(self, flexural_ro, effective_height):
        nominal_moment = self.fy * flexural_ro * self.width * effective_height**2 * (1-0.59*flexural_ro*self.fy/self.fc) * 1000
        return nominal_moment
    

    #Display Methods
    def get_properties(self):
        properties = {}
        for k,v in self.__dict__.items():
            properties[k] = round(v,2)
        return properties

    
    #Region Properties

    @property
    def top_effective_height(self):
        top_effective_height = self.get_effective_height(self.top_rebar_diameter)
        return top_effective_height
    
    @property
    def top_flexural_ro(self):
        top_flexural_ro = self.get_flexural_ro(self.top_total_rebar_area, self.top_effective_height)
        return top_flexural_ro
    
    @property
    def simple_top_nominal_moment_strenght(self):
        simple_top_nominal_moment_strenght = self.get_simple_nominal_moment_strenght(self.top_flexural_ro, self.top_effective_height)
        return simple_top_nominal_moment_strenght

    @property
    def bottom_effective_height(self):
        bottom_effective_height = self.get_effective_height(self.bottom_rebar_diameter)
        return bottom_effective_height
    
    @property
    def bottom_flexural_ro(self):
        bottom_flexural_ro = self.get_flexural_ro(self.bottom_total_rebar_area, self.bottom_effective_height)
        return bottom_flexural_ro
    
    @property
    def simple_bottom_nominal_moment_strenght(self):
        simple_bottom_nominal_moment_strenght = self.get_simple_nominal_moment_strenght(self.bottom_flexural_ro, self.bottom_effective_height)
        return simple_bottom_nominal_moment_strenght
    
    @property
    def nominal_concrete_shear_strenght(self):
        nominal_shear_strenght = 0.17 * sqrt(self.fc) * self.width * self.bottom_effective_height * 1000
        return nominal_shear_strenght
    
    @property
    def nominal_reinforcement_shear_strenght(self):
        reinforcement_shear_strenght = self.stirrup_rebar_area * self.fy * self.bottom_effective_height / self.stirrup_spacing * 1000
        return reinforcement_shear_strenght
    
    @property
    def nominal_shear_strenght(self):
        nominal_shear_strenght = self.nominal_concrete_shear_strenght + self.nominal_reinforcement_shear_strenght
        return nominal_shear_strenght
    

    #Class properties region
    def __str__(self):
        return f"""Reinforced concrete beam properties:
        - Base: {self.width} meters.
        - Height: {self.height} meters.
        - Cover {self.cover} meters.
        - Top reinforcement: {self.top_bars}#{self.top_rebar_diameter} bars.

        """

        

if __name__ == '__main__':
    print("This is not the script you should be executing")

