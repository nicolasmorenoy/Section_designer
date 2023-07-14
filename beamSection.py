#Python imports
from math import sqrt
import drawsvg as draw

from geometry import *
from materials import *
from reinforcement import *


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
    
    @property
    def top_bar_spacing(self) -> float:
        return self.__get_bar_spacing("TOP")
    
    @property
    def bottom_bar_spacing(self) -> float:
        return self.__get_bar_spacing("BOTTOM")
    
    @property
    def top_bars_coordinates(self) -> list:
        return self.__get_bars_x_coordinates("TOP", self.top_bar_spacing )
    
    @property
    def bottom_bars_coordinates(self) -> list:
        return self.__get_bars_x_coordinates("BOTTOM", self.bottom_bar_spacing )
     
        
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
    
    def __get_number_of_bars(self, location) ->int: 
        return sum(self.reinforcement_dict[location]["bar_amount"])
    
    def __get_bar_spacing(self, location) -> float:
        return (self.width-self.cover*2-max(self.reinforcement_dict["TRANSVERSE"]["bar_diameters"])*2-max(self.reinforcement_dict[location]["bar_diameters"]))/(self.__get_number_of_bars(location)-1)
    
    def __get_first_x(self, location) -> float:
        if sum(self.reinforcement_dict[location]["bar_amount"]) == 1:
            return self.width/2
        else:
            return self.reinforcement_dict[location]["bar_diameters"][0]/2+self.reinforcement_dict["TRANSVERSE"]["bar_diameters"][0]+self.cover
    
    def __get_bars_x_coordinates(self, location:str, spacing:float) ->list:
        n=0
        coordinates = []
        for _ in range(sum(self.reinforcement_dict[location]["bar_amount"])):
            coordinates.append(n*spacing+self.__get_first_x(location))
            n+=1
        return coordinates
    
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
    

    def draw_section(self) -> object:
        #//////////////////////////// Must be optimized //////////////////////////
        #Work Area
        d = draw.Drawing(self.width*2000, self.height*2000, origin='center')
        #Stirrups
        s = draw.Rectangle(-(self.width-self.cover*2)*500, -(self.height-self.cover*2)*500, (self.width-self.cover*2)*1000, (self.height-self.cover*2)*1000, fill='none', stroke="#686868", stroke_width=max(self.reinforcement_dict["TRANSVERSE"]["bar_diameters"])*1000)
        s.append_title("Stirrup")
        
        #Gross Section
        ag = draw.Rectangle(-self.width*500, -self.height*500, self.width*1000, self.height*1000, fill='#B0B0B0', stroke='grey')
        ag.append_title("Beam Gross Section")

        #Bars
        ##Corner Bars
        ###Top Bars
        sep_top = max(self.reinforcement_dict["TRANSVERSE"]["bar_diameters"])*500+max(self.reinforcement_dict["TOP"]["bar_diameters"])*500
        tb1 = draw.Circle(-(self.width-self.cover*2)*500+sep_top, -(self.height-self.cover*2)*500+sep_top, max(self.reinforcement_dict["TOP"]["bar_diameters"])*500, fill="black")
        tb2 = draw.Circle((self.width-self.cover*2)*500-sep_top, -(self.height-self.cover*2)*500+sep_top, max(self.reinforcement_dict["TOP"]["bar_diameters"])*500, fill="black")

        sep_bot = max(self.reinforcement_dict["TRANSVERSE"]["bar_diameters"])*500+max(self.reinforcement_dict["BOTTOM"]["bar_diameters"])*500
        bb1 = draw.Circle(-(self.width-self.cover*2)*500+sep_bot, (self.height-self.cover*2)*500-sep_bot, max(self.reinforcement_dict["BOTTOM"]["bar_diameters"])*500, fill="black")
        bb2 = draw.Circle((self.width-self.cover*2)*500-sep_bot, (self.height-self.cover*2)*500-sep_bot, max(self.reinforcement_dict["BOTTOM"]["bar_diameters"])*500, fill="black")


        d.append(ag)
        d.append(s)
        d.append(tb1)
        d.append(tb2)
        d.append(bb1)
        d.append(bb2)

        return d
    ##Minimum reinforcement

    def minimum_reinforcement_ratio(self) -> float:
        return round(max(0.25*sqrt(self.concrete.fc),1.4)/self.steel.fy,4)
    
    def minimum_top_area(self) -> float:
        return self.minimum_reinforcement_ratio()*self.top_effective_height[0]*self.width
    
    def minimum_bottom_area(self) -> float:
        return self.minimum_reinforcement_ratio()*self.bottom_effective_height[0]*self.width
    
    #Display Methods
    def get_strength(self):
        return{
        "Top nominal moment strength": str(round(self.simple_top_nominal_moment_strength,2))+ "kN-m.",
        "Bottom nominal moment strength": str(round(self.simple_bottom_nominal_moment_strength, 2)) + "kN-m.",
        "Shear nominal strength": str(round(self.nominal_shear_strength))+"kN."
        }

    def get_design_properties(self):
        return{
            "effective depth, d_top": str(round(self.top_effective_height[0],2))+ " m.",
            "effective depth, d_bottom": str(round(self.top_effective_height[0],2))+ " m.",
            "top flexural ratio, ro": str(round(self.sum_top_flexural_ro,4)),
            "bottom flexural ratio, ro": str(round(self.sum_bottom_flexural_ro,4))

        }
    
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

