#Python imports
from math import pi, sqrt


#Geometry Section

class Rectangular:
    """
    - Title: 
    Rectangular
    - Description:
        Class created as a category for a rectangular cross secction geometry of an element.
    - Parameters:
        - Lenght 1, 2: The two dimension of the cross rectangular section [m].
    -  Properties:
        - Cross sectional Area [m²].
        - Moment of Inertia around axis 1 and axis 2 [m⁴].
    """
    def __init__(self, lenght_1, lenght_2):
        self.lenght_1 = lenght_1
        self.lenght_2 = lenght_2
        

    @property
    def cross_area(self):
        cross_area = self.lenght_1 * self.lenght_2
        return cross_area
    

    @property
    def moment_inertia_11(self):
        moment_inertia_11 = self.lenght_1*self.lenght_2**3/12
        return moment_inertia_11
    

    @property
    def moment_inertia_22(self):
        moment_inertia_22 = self.lenght_2*self.lenght_1**3/12
        return moment_inertia_22
    

class Circular:
    """
    - Title: 
    Circular
    - Description:
        Class created as a category for a circular cross secction geometry of an element.
    - Parameters:
        - Diameter of the cross rectangular section [m].
    - Properties:
        - Cross sectional Area [m²].
        - Moment of Inertia(pending) [m⁴].
    """

    def __init__(self, diameter):
        self.diameter = diameter
    

    @property
    def cross_area(self):
        cross_area = self.diameter**2*pi/4
        return cross_area


#Region Materials
class Concrete:
    """
    - Title: 
    Concrete
    - Description:
    Class that describe the physical properties of the Concrete.
    - Parameters:
        - f'c = specified compressive strength og concrete [MPa]
        - εcu = maximum usable strain at extreme concrete compression fiber
    - Properties:
        -Modulus of elasticity of concrete [MPa].
    """


    def __init__(self, fc = 28, εcu = 0.003):
        self.fc = fc
        self.εcu = εcu
    
    
    @property
    def elastic_modulus(self, EC_factor = 3900):
        elastic_modulus = EC_factor*sqrt(self.fc)
        return elastic_modulus

class Steel:
    """
    - Title: 
    Steel
    - Description:
    Class that describe the physical properties of the Steel.
    - Parameters:
        - fy = specified yield strength of reinforcement [MPa]
        - ES = Modulus of elasticity of reinforcement [MPa]
    """

    def __init__(self, fy = 420, ES = 200000):
        self.fy = fy
        self.ES = ES
   

#Reinforcement
class Reinforcement:
    """
    - Title: 
    Reinforcement
    - Description:
    Class that took the diameter and gives back the properties of the cross section of reinforcement.
    - Parameters:
        - bar number = Number of the bar acording to the US Standar : #/8
    - Properties:
        - bar diameter = Diameter of the bar that correspond to the number of the bar divide by 8 and then multiplied for 0.0254 m [m].
        - bar area = Cross sectional Area of the bar [m²].
    """

    def __init__(self, bar_number):
        self.bar_number = bar_number
    
    @property
    def diameter(self):
        diameter = self.bar_number/8*.0254
        return diameter

    @property
    def area(self):
        area = Circular(self.diameter).cross_area
        return area

class TransverseReinforcement(Reinforcement):
    """
    - Title: 
    Trasnverse Reinforcement
    - Description:
    Class that inherits the cross section properties of the Reinforcement Class and adds a new parameter (spacing)
    - Parameters:
        - bar number = Number of the bar acording to the US Standar : #/8
        - spacing: longitudinal spacing of the transverse reinforcement.
    - Properties:
        - bar diameter = Diameter of the bar that correspond to the number of the bar divide by 8 and then multiplied for 0.0254 m [m].
        - bar area = Cross sectional Area of the bar [m²].
    """

    def __init__(self, bar_number, spacing):
        self.spacing = spacing
        super().__init__(bar_number)
    

class ReinforcementProperties:
    """
    - Title: 
    Reinforcement Properties
    - Description:
    Class that gives the total amount of rebar area. 
    - Parameters:
        - bar amount = Amount of reinforcement bars. [Number]
        - reinforcement: Instance of the Reinforcement or Transverse Reinforcement class.
    - Properties:
        - total rebar area = Cross sectional Area of the total amount of rebar [m²].
    """

    def __init__(self, bar_amount, reinforcement):
        self.bar_amount = bar_amount
        self.reinforcement = reinforcement
    
    @property
    def area(self):
        area = self.bar_amount * self.reinforcement.area
        return area
        
           

#Section designer region
class Beam:
    """
    - Title: 
    Reinforcement Properties
    - Description:
    Class that gives the total amount of rebar area. 
    - Parameters:
        - bar amount = Amount of reinforcement bars. [Number]
        - reinforcement: Instance of the Reinforcement or Transverse Reinforcement class.
    - Properties:
        - total rebar area = Cross sectional Area of the total amount of rebar [m²].
    """

    def __init__(self, cross_section, span_lenght, cover, concrete, steel, top_reinforcement, bottom_reinforcement, stirrups):
        self.width = cross_section.lenght_1
        self.height = cross_section.lenght_2
        self.span_lenght = span_lenght
        self.cover = cover
        self.fc = concrete.fc
        self.fy = steel.fy
        self.top_reinforcement = top_reinforcement
        self.bottom_reinforcement = bottom_reinforcement
        self.stirrups = stirrups
    

    #Region Methods
    #Get Properties Methods
       
    def get_effective_height(self, reinforcement_diameter):
        effective_height = self.height - self.cover - self.stirrups.reinforcement.diameter - reinforcement_diameter/2
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
        top_effective_height = self.get_effective_height(self.top_reinforcement.reinforcement.diameter)
        return top_effective_height
    
    @property
    def top_flexural_ro(self):
        top_flexural_ro = self.get_flexural_ro(self.top_reinforcement.area, self.top_effective_height)
        return top_flexural_ro
    
    @property
    def simple_top_nominal_moment_strenght(self):
        simple_top_nominal_moment_strenght = self.get_simple_nominal_moment_strenght(self.top_flexural_ro, self.top_effective_height)
        return simple_top_nominal_moment_strenght

    @property
    def bottom_effective_height(self):
        bottom_effective_height = self.get_effective_height(self.bottom_reinforcement.reinforcement.diameter)
        return bottom_effective_height
    
    @property
    def bottom_flexural_ro(self):
        bottom_flexural_ro = self.get_flexural_ro(self.bottom_reinforcement.area, self.bottom_effective_height)
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
        reinforcement_shear_strenght = self.stirrups.area * self.fy * self.bottom_effective_height / self.stirrups.reinforcement.spacing * 1000
        return reinforcement_shear_strenght
    
    @property
    def nominal_shear_strenght(self):
        nominal_shear_strenght = self.nominal_concrete_shear_strenght + self.nominal_reinforcement_shear_strenght
        return nominal_shear_strenght
    

    ##Change Properties Methods

    @simple_bottom_nominal_moment_strenght.setter
    def simple_bottom_nominal_moment_strenght(self,reinforcement):
        self.top_reinforcement = reinforcement
    

    @top_flexural_ro.setter
    def top_flexural_ro(self,reinforcement):
        self.top_reinforcement = reinforcement
    

    #Class properties region
    # def __str__(self):
    #     return f"""Reinforced concrete beam properties:
    #     - Base: {self.width} meters.
    #     - Height: {self.height} meters.
    #     - Cover {self.cover} meters.
    #     - Top reinforcement: {self.top_bars}#{self.top_rebar_diameter} bars.

    #     """

        

if __name__ == '__main__':
    print("This is not the script you should be executing")

