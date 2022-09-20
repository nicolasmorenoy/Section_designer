from classes import Beam, Reinforcement, ReinforcementProperties, Rectangular, Concrete, Steel, TransverseReinforcement

top_rebar= ReinforcementProperties(2,Reinforcement(5))
bottom_rebar = ReinforcementProperties(2,Reinforcement(5))
stirrup_rebar = ReinforcementProperties(2,TransverseReinforcement(3, 0.2))
concrete = Concrete(28)
steel = Steel(420)
geometry = Rectangular(0.3,0.4)
beam = Beam(geometry, 5, 0.04, concrete,steel, top_rebar, bottom_rebar, stirrup_rebar)



if __name__ == '__main__':
    print (beam.simple_top_nominal_moment_strenght)
    top_rebar= ReinforcementProperties(2,Reinforcement(6))
    print (beam.simple_top_nominal_moment_strenght)

    #print(beam.rebar.top_rebar_diameter, beam.rebar.top_rebar_area*10000, beam.top_effective_height, beam.simple_top_nominal_moment_strenght, beam.simple_bottom_nominal_moment_strenght, beam.nominal_shear_strenght)