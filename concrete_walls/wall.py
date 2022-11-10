class WallSection():
    def __init__(self, name) -> None:
        self.name = name
    
    #Inputs
    ## Geometry Input
       
    def get_geometry(self, width: float, lenght: float, height: float):
        self.width = width
        self.lenght = lenght
        self.height = height
    
    def get_recover(self, recover: float):
        self.recover = recover
    
    ## Materials Input
    
    def get_concrete(self, fc: float = 28.0):
        self.fc = fc
        self.EC = 3900*(self.fc)**0.5
        self.ec = 0.003
    
    def get_steel(self, fy:float = 420.0):
        self.fy = fy
        self.ES = 200000
        self.ey = self.fy/self.ES
    
    ## Reinforcement Input    
    
    


class Wall():
    def __init__(self, name) -> None:
        self.name = name
        self.sections = {}
    
    def get_sections(self, section: WallSection):
        self.section = section

    
        