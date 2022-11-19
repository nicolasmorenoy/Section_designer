from classes import BeamSection, Rebar, Reinforcement, Rectangular, Concrete, Steel, TransverseRebar

top_rebar= Reinforcement(2,Rebar(5))
bottom_rebar= Reinforcement(2,Rebar(5))
stirrup_rebar = Reinforcement(2,TransverseRebar(3, 0.2))
concrete = Concrete(28, EC_factor=3900)
steel = Steel(420)
geometry = Rectangular(0.4,0.4)
beam = BeamSection("id")
beam.get_concrete(concrete)
beam.get_cover(0.04)
beam.get_reinforcement(top_rebar, "Top")
beam.get_reinforcement(bottom_rebar, "Bottom")
beam.get_reinforcement(stirrup_rebar, "Stirrups")
beam.get_steel(steel)
beam.get_section(geometry)




if __name__ == '__main__':
    print(beam)