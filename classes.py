#Python imports
from math import pi, sqrt
from enum import Enum



#Geometry Section

class GeometryType(Enum):
    """
    - Title:
    GeometryType
    - Description:
        Class created to enumerate the geometric sections for the elements.
    - Parameters:
        None
    """
    RECTANGULAR = 1
    CIRCULAR = 1

class Geometry:
    """
    - Title:
    Geometry
    - Description:
        Class created to encapsulate all the geometric sections.
    - Parameters:
        Geometry Type [Class]
    """
    def __init__(self, geometry_section: GeometryType) -> None:
        self.geometry = geometry_section


class Rectangular(Geometry):
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
        super().__init__(GeometryType.RECTANGULAR)
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
    
    
    def __dict__(self):
        return {
            "length 1": str(round(self.lenght_1,2))+" m",
            "length 2":str(round(self.lenght_2,2))+" m",
            "gross area, Ag": str(round(self.cross_area, 4))+" m²",
            "moment of inertia 1-1, Ig 1-1": str(round(self.moment_inertia_11,6))+ " m4",
            "moment of inertia 2-2, Ig 2-2": str(round(self.moment_inertia_22,6))+ " m4",
            "centroid 1-1": str(round(self.centroid11,2))+" m",
            "centroid 2-2": str(round(self.centroid22,2))+" m"
            }
    

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
class ReinforcementLocationType(Enum):
    """
    - Title:
    ReinforcementLocationType
    - Description:
        Class created to enumerate the Reinforcement possible location on the element.
    - Parameters:
        None
    """
    TOP = 1
    BOTTOM = 2
    TRANSVERSE = 3

class ReinforcementLocation():
    """
    - Title:
    Geometry
    - Description:
        Class created to encapsulate the location of the reinforcement in the element.
    - Parameters:
        Reinforcement location Type [Class]
    """
    def __init__(self, reinforcement_location: ReinforcementLocationType) -> None:
        self.location = reinforcement_location
        
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
        - bar diameter = Diameter of the bar that correspond to the number of the bar divide by 8 and then multiplied for 0.0254 [m].
        - bar area = Cross sectional Area of the bar [m²].
    """

    def __init__(self, bar_number: int, spacing: float) -> None:
        self.spacing = spacing
        super().__init__(bar_number)
    

class Reinforcement(ReinforcementLocation):
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

    def __init__(self, bar_amount: int, reinforcement: Rebar, location: ReinforcementLocationType) -> None:
        self.bar_amount = bar_amount
        self.reinforcement = reinforcement
        super().__init__(location)
    
    @property
    def area(self) ->float:
        return self.bar_amount * self.reinforcement.area
            

#Section designer region
class BeamSection:
    """
    - Title: 
    Beam
    - Description:
    Class that gives all the properties for a beam section given an especific input. 
    - Parameters:
        - cross section = Rectangular or Circular class acording to the geometry. [Class isntance]
        - span lenght = Span lenght of the beam [m]
        - cover = Cover of the beam from the external face to the transverse reinforcement. [m]
        - concrete = Concrete class [Class isntance]
        - steel = Steel class [Class isntance]
        - top_reinforcement = Reinforcement class instance that indicates the top reinforcement of the beam [Class isntance]
        - bottom_reinforcement = Reinforcement class that instance indicates the bottom reinforcement of the beam [Class isntance]
        - stirrups = Reinforcement class that instance indicates the stirrups reinforcement of the beam [Class isntance]

    - Properties:
        - total rebar area = Cross sectional Area of the total amount of rebar [m²].
    """
    def __init__(self, id: str):
        self.id = id
        self.reinforcement_dict = {}

    #Region Get Properties
    def set_section(self, cross_section: Rectangular):
        self.cross_section = cross_section
        self.width = cross_section.lenght_1
        self.height = cross_section.lenght_2
        self.area = cross_section.cross_area
       
    def set_cover(self, cover: float):
        self.cover = cover
    
    def set_concrete(self, concrete: Concrete):
        self.concrete = concrete
    
    def set_steel(self, steel: Steel):
        self.steel = steel
    
    def set_reinforcement(self, reinforcement: Reinforcement):
        self.reinforcement_dict[reinforcement.location.name] = {
            "bar_amount":[reinforcement.bar_amount,],
            "bar_area":[reinforcement.area,],
            "bar_diameters":[reinforcement.reinforcement.diameter,],
            "bar_number":[reinforcement.reinforcement.bar_number,]
        }
        if reinforcement.location == ReinforcementLocationType.TRANSVERSE:
            self.reinforcement_dict[reinforcement.location.name]["spacing"] = reinforcement.reinforcement.spacing

    
    def set_aditional_reinforcement(self, reinforcement: Reinforcement):
        self.reinforcement_dict[reinforcement.location.name]["bar_amount"].append(reinforcement.bar_amount)
        self.reinforcement_dict[reinforcement.location.name]["bar_area"].append(reinforcement.area)
        self.reinforcement_dict[reinforcement.location.name]["bar_diameters"].append(reinforcement.reinforcement.diameter)
        self.reinforcement_dict[reinforcement.location.name]["bar_number"].append(reinforcement.reinforcement.bar_number)

        if reinforcement.location == ReinforcementLocationType.TRANSVERSE:
            self.reinforcement_dict[reinforcement.location.name]["spacing"] = reinforcement.reinforcement.spacing

    #Region Properties
    ## Geometry Properties
    @property
    def top_effective_height(self) ->float:
        return list(map(self.__get_effective_height, self.reinforcement_dict["TOP"]["bar_diameters"])) 
    
    @property
    def bottom_effective_height(self) ->float:      
        return list(map(self.__get_effective_height, self.reinforcement_dict["BOTTOM"]["bar_diameters"]))
    
    @property
    def top_cracked_inertia(self) ->float:
        return Rectangular(self.width, self.top_cracked_section_centroid).moment_inertia_11 + self.width * self.top_cracked_section_centroid * (self.top_cracked_section_centroid/2)** 2 + (self.elastic_modulus_ratio-1)*sum(self.reinforcement_dict["TOP"]["bar_area"])* (max(self.top_effective_height)-self.top_cracked_section_centroid)**2
    
    @property
    def bottom_cracked_inertia(self) ->float:
        return Rectangular(self.width, self.bottom_cracked_section_centroid).moment_inertia_11 + self.width * self.bottom_cracked_section_centroid * (self.bottom_cracked_section_centroid/2)** 2 + (self.elastic_modulus_ratio-1)*sum(self.reinforcement_dict["BOTTOM"]["bar_area"])* (max(self.bottom_effective_height)-self.bottom_cracked_section_centroid)**2
    
    #This can be improved if we calculated it including the opposite reinforcement in the beam
    @property
    def top_cracked_section_centroid(self) ->float:
        return max(self.top_effective_height)*(sqrt((self.elastic_modulus_ratio*self.sum_top_flexural_ro)**2+2*self.elastic_modulus_ratio*self.sum_top_flexural_ro)-self.elastic_modulus_ratio*self.sum_top_flexural_ro)
    
    @property
    def bottom_cracked_section_centroid(self) ->float:
        return max(self.bottom_effective_height)*(sqrt((self.elastic_modulus_ratio*self.sum_bottom_flexural_ro)**2+2*self.elastic_modulus_ratio*self.sum_bottom_flexural_ro)-self.elastic_modulus_ratio*self.sum_bottom_flexural_ro)

    ##Reinforcement Properties
    @property
    def top_flexural_ro(self) ->float:
        return list(map(self.__get_flexural_ro,self.reinforcement_dict["TOP"]["bar_area"], self.top_effective_height))
    
    @property
    def sum_top_flexural_ro(self) ->float:
        return sum(self.top_flexural_ro)
    
    @property
    def bottom_flexural_ro(self) ->float:
        return list(map(self.__get_flexural_ro,self.reinforcement_dict["BOTTOM"]["bar_area"], self.bottom_effective_height))
    
    @property
    def sum_bottom_flexural_ro(self) ->float:
        return sum(self.bottom_flexural_ro)
    
    @property
    def elastic_modulus_ratio(self) ->float:
        return self.steel.ES/self.concrete.elastic_modulus
    
    ##Nominal Resistance
    @property
    def simple_top_nominal_moment_strength(self) ->float:
        return sum(list(map(self.__get_simple_nominal_moment_strength,self.top_flexural_ro, self.top_effective_height)))

    @property
    def simple_bottom_nominal_moment_strength(self) ->float:
        return sum(list(map(self.__get_simple_nominal_moment_strength,self.bottom_flexural_ro, self.bottom_effective_height)))
    
    @property
    def nominal_concrete_shear_strength(self) ->float:
        return 0.17 * sqrt(self.concrete.fc) * self.width * max(self.bottom_effective_height) * 1000
    
    @property
    def nominal_reinforcement_shear_strength(self) ->float:
        return sum(self.reinforcement_dict["TRANSVERSE"]["bar_area"]) * self.steel.fy * max(self.bottom_effective_height) / self.reinforcement_dict["TRANSVERSE"]["spacing"] * 1000
    
    @property
    def nominal_shear_strength(self) ->float:
        return self.nominal_concrete_shear_strength + self.nominal_reinforcement_shear_strength
    
    ##Cracked Section
    @property
    def cracking_moment(self) ->float:
        return self.concrete.cracking_stress * self.cross_section.moment_inertia_11 / (self.height-self.cross_section.centroid22) * 1000
    
    @property
    def top_lambda_delta(self) -> float:
        return self.__get_lambda_delta(self.sum_bottom_flexural_ro)
    
    @property
    def bottom_lambda_delta(self) -> float:
        return self.__get_lambda_delta(self.sum_top_flexural_ro)
    
    
   
        
 #Region Methods
    ##Internal Methods
       
    def __get_effective_height(self, reinforcement_diameter: float) ->float:
        return self.height - self.cover - max(self.reinforcement_dict["TRANSVERSE"]["bar_diameters"]) - reinforcement_diameter/2
    
    def __get_flexural_ro(self, rebar_area:float, effective_height: float) ->float:
        return rebar_area/(self.width*effective_height)

    def __get_simple_nominal_moment_strength(self, flexural_ro: float, effective_height: float) ->float:
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
    
    def display_geometry(self) -> float:
        return {
            "width": self.width,
            "height": self.height,
            "area": self.cross_section.cross_area
        } 
    
    ##Minimum reinforcement

    def minimum_reinforcement_ratio(self) -> float:
        return round(max(0.25*sqrt(self.concrete.fc),1.4)/self.steel.fy,4)
    
    def minimum_top_area(self) -> float:
        return self.minimum_reinforcement_ratio()*self.top_effective_height[0]*self.width
    
    def minimum_bottom_area(self) -> float:
        return self.minimum_reinforcement_ratio()*self.bottom_effective_height[0]*self.width
    
    #Display Methods
    def get_strength(self):
        return{"Top nominal moment strength": str(round(self.simple_top_nominal_moment_strength,2))+ "kN-m.",
        "Bottom nominal moment strength": str(round(self.simple_bottom_nominal_moment_strength, 2)) + "kN-m.",
        "Shear nominal strength": str(round(self.nominal_shear_strength))+"kN."}

    
    ##Change Properties Methods

    @simple_bottom_nominal_moment_strength.setter
    def simple_bottom_nominal_moment_strength(self,reinforcement):
        self.top_reinforcement = reinforcement
    

    @top_flexural_ro.setter
    def top_flexural_ro(self,reinforcement):
        self.top_reinforcement = reinforcement
    

    


    

    #Class properties region
    # def __str__(self):
    #     return f"""Reinforced concrete beam properties:
    #     Geometry:
    #     - Base: {self.width} meters.
    #     - Height: {self.height} meters.
    #     - Cover {self.cover} meters.
        
    #     Reinforcement:
    #     - Top reinforcement: {self.bottom_reinforcement.bar_amount} bar #{self.bottom_reinforcement.reinforcement.bar_number}.
    #     - Bottom reinforcement: {self.bottom_reinforcement.bar_amount} bar #{self.bottom_reinforcement.reinforcement.bar_number}.
    #     - Stirrups: {self.stirrups.bar_amount} legs #{self.stirrups.reinforcement.bar_number} spacing: {self.stirrups.reinforcement.spacing} m.
        
    #     Materials:
    #     - Concrete f'c: {self.concrete.fc}
    #     - Steel Reinforcement fy: {self.steel.fy}

    #     Nominal Properties:
    #     - Top nominal moment strength: {round(self.simple_top_nominal_moment_strength,2)} kN-m.
    #     - Bottom nominal moment strength: {round(self.simple_bottom_nominal_moment_strength, 2)} kN-m.
    #     - Shear nominal strength: {round(self.nominal_shear_strength)} kN.
    #     """

    # def __str__(self):
    #     return f"""Reinforced concrete beam properties:
    #     Nominal Properties:
    #     - Top nominal moment strength: {round(self.simple_top_nominal_moment_strength,2)} kN-m.
    #     - Bottom nominal moment strength: {round(self.simple_bottom_nominal_moment_strength, 2)} kN-m.
    #     - Shear nominal strength: {round(self.nominal_shear_strength)} kN.
    #     """
    
    def __dict__(self):
        return{"Top nominal moment strength": str(round(self.simple_top_nominal_moment_strength,2))+ "kN-m.",
        "Bottom nominal moment strength": str(round(self.simple_bottom_nominal_moment_strength, 2)) + "kN-m.",
        "Shear nominal strength": str(round(self.nominal_shear_strength))+"kN."}

        

if __name__ == '__main__':
    print("This is not the script you should be executing")

