from classes import BeamSection, Rebar, Reinforcement, Rectangular, Concrete, Steel, TransverseRebar, ReinforcementLocationType

top_rebar= Reinforcement(2,Rebar(5),ReinforcementLocationType.TOP)
bottom_rebar= Reinforcement(3,Rebar(5),ReinforcementLocationType.BOTTOM)
stirrup_rebar = Reinforcement(2,TransverseRebar(3, 0.2),ReinforcementLocationType.TRANSVERSE)
concrete = Concrete(28, EC_factor=3900)
steel = Steel(420)
geometry = Rectangular(0.4,0.4)
beam = BeamSection("id")
beam.get_concrete(concrete)
beam.get_cover(0.04)
beam.get_reinforcement(top_rebar)
beam.get_reinforcement(bottom_rebar)
beam.get_reinforcement(stirrup_rebar)
beam.get_steel(steel)
beam.get_section(geometry)




if __name__ == '__main__':
    print(beam)
    beam.get_aditional_reinforcement(Reinforcement(3,Rebar(5),ReinforcementLocationType.TOP))
    print(beam)
    top_rebar= Reinforcement(5,Rebar(5),ReinforcementLocationType.TOP)
    beam.get_reinforcement(top_rebar)
    print(beam)
