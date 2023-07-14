#Python imports
from math import sqrt, pi
from enum import Enum

#Package imports
import geometry

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
   
