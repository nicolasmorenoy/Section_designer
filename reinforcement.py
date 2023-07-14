#Python imports
from math import sqrt
from enum import Enum

#Package imports
from geometry import *

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
            
