#Python imports
from math import pi
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