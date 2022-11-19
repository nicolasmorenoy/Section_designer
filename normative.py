from enum import Enum

class Normatives(Enum):
    NSR = 1
    ACI318 = 2

class NSR(Enum):
    NSR_10 = 1

class ACI318(Enum):
    ACI318_19 = 1


class NSR_10():
    def __init__(self) -> None:
        pass