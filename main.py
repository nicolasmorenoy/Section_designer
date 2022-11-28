from classes import BeamSection, Rebar, Reinforcement, Rectangular, Concrete, Steel, TransverseRebar, ReinforcementLocationType

top_rebar= Reinforcement(2,Rebar(5),ReinforcementLocationType.TOP)
bottom_rebar= Reinforcement(3,Rebar(5),ReinforcementLocationType.BOTTOM)
stirrup_rebar = Reinforcement(2,TransverseRebar(3, 0.2),ReinforcementLocationType.TRANSVERSE)
concrete = Concrete(28, EC_factor=3900)
steel = Steel(420)
geometry = Rectangular(0.4,0.4)
beam = BeamSection("id")
beam.set_concrete(concrete)
beam.set_cover(0.04)
beam.set_reinforcement(top_rebar)
beam.set_reinforcement(bottom_rebar)
beam.set_reinforcement(stirrup_rebar)
beam.set_steel(steel)
beam.set_section(geometry)




if __name__ == '__main__':
    print(beam)
    beam.set_aditional_reinforcement(Reinforcement(1,Rebar(6),ReinforcementLocationType.TOP))
    beam.set_aditional_reinforcement(Reinforcement(1,Rebar(6),ReinforcementLocationType.BOTTOM))
    print(beam)
    # top_rebar= Reinforcement(5,Rebar(5),ReinforcementLocationType.TOP)
    # beam.get_reinforcement(top_rebar)
    # print(beam)
