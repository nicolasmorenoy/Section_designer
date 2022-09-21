from classes import Beam, Rebar, Reinforcement, Rectangular, Concrete, Steel, TransverseRebar

top_rebar= Reinforcement(2,Rebar(5))
bottom_rebar = Reinforcement(2,Rebar(5))
stirrup_rebar = Reinforcement(2,TransverseRebar(3, 0.2))
concrete = Concrete(28)
steel = Steel(420)
geometry = Rectangular(0.3,0.4)
beam = Beam(geometry, 5, 0.04, concrete,steel, top_rebar, bottom_rebar, stirrup_rebar)



if __name__ == '__main__':
    print (beam.top_flexural_ro, beam.simple_top_nominal_moment_strenght)
    beam.top_flexural_ro = Reinforcement(3,Rebar(5))
    print (beam.top_flexural_ro, beam.simple_top_nominal_moment_strenght)
    print(beam.get_properties())