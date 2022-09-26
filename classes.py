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
    def __init__(self, lenght_1: float, lenght_2: float) -> None:
        self.lenght_1 = lenght_1
        self.lenght_2 = lenght_2
        

    @property
    def cross_area(self) ->float:
        return self.lenght_1 * self.lenght_2
    

    @property
    def moment_inertia_11(self) -> float:
        return self.lenght_1*self.lenght_2**3/12
    

    @property
    def moment_inertia_22(self) -> float:
        return self.lenght_2*self.lenght_1**3/12
    
    @property
    def centroid11(self) -> float:
        return self.lenght_1 / 2
    
    @property
    def centroid22(self) -> float:
        return self.lenght_2 / 2
    

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

    def __init__(self, diameter: float) -> None:
        self.diameter = diameter
    

    @property
    def cross_area(self) ->float:
        return self.diameter**2*pi/4
    
    @property
    def centroid11(self) -> float:
        return self.diameter / 2
    
    @property
    def centroid22(self) -> float:
        return self.diameter / 2


#Region Materials
class Concrete:
    """
    - Title: 
    Concrete
    - Description:
    Class that describe the physical properties of the Concrete.
    - Parameters:
        - f'c = specified compressive strength og concrete [MPa]
        - ecu = maximum usable strain at extreme concrete compression fiber
    - Properties:
        -Modulus of elasticity of concrete [MPa].
        -Cracking stress of concrete
    """


    def __init__(self, fc: float = 28, ecu: float = 0.003, EC_factor: int = 3900) -> None:
        self.fc = fc
        self.ecu = ecu
        self.EC_factor = EC_factor
    
    
    @property
    def elastic_modulus(self) ->float:
        return self.EC_factor*sqrt(self.fc)
    
    @property
    def cracking_stress(self) -> float:
        return 0.62*sqrt(self.fc)

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

    def __init__(self, fy: float = 420, ES: float = 200000) -> None:
        self.fy = fy
        self.ES = ES
   

#Reinforcement
class Rebar:
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

    def __init__(self, bar_number: int) -> None:
        self.bar_number = bar_number
    
    @property
    def diameter(self) ->float:
        return self.bar_number/8*.0254

    @property
    def area(self) ->float:
        return Circular(self.diameter).cross_area

class TransverseRebar(Rebar):
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

    def __init__(self, bar_number: int, spacing: float) -> None:
        self.spacing = spacing
        super().__init__(bar_number)
    

class Reinforcement:
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

    def __init__(self, bar_amount: int, reinforcement: Rebar) -> None:
        self.bar_amount = bar_amount
        self.reinforcement = reinforcement
    
    @property
    def area(self) ->float:
        return self.bar_amount * self.reinforcement.area
        
           

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

    def __init__(self, cross_section: Rectangular, span_lenght: float, cover: float, concrete: Concrete, steel: Steel, top_reinforcement: Reinforcement, bottom_reinforcement: Reinforcement, stirrups: Reinforcement) -> None:
        self.cross_section = cross_section
        self.width = cross_section.lenght_1
        self.height = cross_section.lenght_2
        self.span_lenght = span_lenght
        self.cover = cover
        self.concrete = concrete
        self.steel = steel
        self.top_reinforcement = top_reinforcement
        self.bottom_reinforcement = bottom_reinforcement
        self.stirrups = stirrups
    

    #Region Properties
    ## Geometry Properties
    @property
    def top_effective_height(self) ->float:
        return self.__get_effective_height(self.top_reinforcement.reinforcement.diameter)
    
    @property
    def bottom_effective_height(self) ->float:
        return self.__get_effective_height(self.bottom_reinforcement.reinforcement.diameter)
    
    @property
    def top_cracked_inertia(self) ->float:
        return Rectangular(self.width, self.top_cracked_section_centroid).moment_inertia_11 + self.width * self.top_cracked_section_centroid * (self.top_cracked_section_centroid/2)** 2 + self.elastic_modulus_ratio*self.top_reinforcement.area * (self.top_effective_height-self.top_cracked_section_centroid)**2
    
    @property
    def bottom_cracked_inertia(self) ->float:
        return Rectangular(self.width, self.bottom_cracked_section_centroid).moment_inertia_11 + self.width * self.bottom_cracked_section_centroid * (self.bottom_cracked_section_centroid/2)** 2 + self.elastic_modulus_ratio*self.bottom_reinforcement.area * (self.bottom_effective_height-self.bottom_cracked_section_centroid)**2
    
    #This can be improved if we calculated it including the opposite reinforcement in the beam
    @property
    def top_cracked_section_centroid(self) ->float:
        return self.top_effective_height*(sqrt((self.elastic_modulus_ratio*self.top_flexural_ro)**2+2*self.elastic_modulus_ratio*self.top_flexural_ro)-self.elastic_modulus_ratio*self.top_flexural_ro)
    
    @property
    def bottom_cracked_section_centroid(self) ->float:
        return self.bottom_effective_height*(sqrt((self.elastic_modulus_ratio*self.bottom_flexural_ro)**2+2*self.elastic_modulus_ratio*self.bottom_flexural_ro)-self.elastic_modulus_ratio*self.bottom_flexural_ro)

    ##Reinforcement Properties
    @property
    def top_flexural_ro(self) ->float:
        return self.__get_flexural_ro(self.top_reinforcement.area, self.top_effective_height)
    
    @property
    def bottom_flexural_ro(self) ->float:
        return self.__get_flexural_ro(self.bottom_reinforcement.area, self.bottom_effective_height)
    
    @property
    def elastic_modulus_ratio(self) ->float:
        return self.steel.ES/self.concrete.elastic_modulus
    
    ##Nominal Resistance
    @property
    def simple_top_nominal_moment_strenght(self) ->float:
        return self.__get_simple_nominal_moment_strenght(self.top_flexural_ro, self.top_effective_height)

    @property
    def simple_bottom_nominal_moment_strenght(self) ->float:
        return self.__get_simple_nominal_moment_strenght(self.bottom_flexural_ro, self.bottom_effective_height)
    
    @property
    def nominal_concrete_shear_strenght(self) ->float:
        return 0.17 * sqrt(self.concrete.fc) * self.width * self.bottom_effective_height * 1000
    
    @property
    def nominal_reinforcement_shear_strenght(self) ->float:
        return self.stirrups.area * self.steel.fy * self.bottom_effective_height / self.stirrups.reinforcement.spacing * 1000
    
    @property
    def nominal_shear_strenght(self) ->float:
        return self.nominal_concrete_shear_strenght + self.nominal_reinforcement_shear_strenght
    
    ##Cracked Section
    @property
    def cracking_moment(self) ->float:
        return self.concrete.cracking_stress * self.cross_section.moment_inertia_11 / (self.height-self.cross_section.centroid22) * 1000
    
    @property
    def top_lambda_delta(self) -> float:
        return self.__get_lambda_delta(self.bottom_flexural_ro)
    
    @property
    def bottom_lambda_delta(self) -> float:
        return self.__get_lambda_delta(self.top_flexural_ro)
    
    
   
        
 #Region Methods
    ##Internal Methods
       
    def __get_effective_height(self, reinforcement_diameter: float) ->float:
        return self.height - self.cover - self.stirrups.reinforcement.diameter - reinforcement_diameter/2
    
    def __get_flexural_ro(self, rebar_area, effective_height: float) ->float:
        return rebar_area/(self.width*effective_height)

    def __get_simple_nominal_moment_strenght(self, flexural_ro: float, effective_height: float) ->float:
        return self.steel.fy * flexural_ro * self.width * effective_height**2 * (1-0.59*flexural_ro*self.steel.fy/self.concrete.fc) * 1000
    
    def __get__effective_inertia(self, Ma: float, Icr: float) ->float:
        return (self.cracking_moment/Ma)**3 * self.cross_section.moment_inertia_11 + (1 - (self.cracking_moment/Ma)**3) * Icr
    
    def __get_lambda_delta(self, ro) ->float:
        return 1/(1+50*ro)
    
    #Get Properties Methods
    def top_effective_inertia(self, Ma) -> float:
        if self.__get__effective_inertia(Ma, self.top_cracked_inertia) > self.cross_section.moment_inertia_11:
            return self.cross_section.moment_inertia_11
        else:
            return self.__get__effective_inertia(Ma, self.top_cracked_inertia)
    
    def bottom_effective_inertia(self, Ma) -> float:
        if self.__get__effective_inertia(Ma, self.bottom_cracked_inertia) > self.cross_section.moment_inertia_11:
            return self.cross_section.moment_inertia_11
        else:
            return self.__get__effective_inertia(Ma, self.bottom_cracked_inertia)
    
    def top_deflexion_multiplier(self, Ma) -> float:
        return self.top_lambda_delta/(self.top_effective_inertia(Ma)/self.cross_section.moment_inertia_11)
    
    def bottom_deflexion_multiplier(self, Ma) -> float:
        return self.top_lambda_delta/(self.top_effective_inertia(Ma)/self.cross_section.moment_inertia_11)
    
    


    
    
    
    
     

    #Display Methods
    def get_properties(self):
        properties = {}
        for k,v in self.__dict__.items():
            properties[k] = v
        return properties

    
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

