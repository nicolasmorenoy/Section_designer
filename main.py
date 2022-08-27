from classes import Beam, Rebar, ReinforcementProperties, Rectangular, Concrete, Steel

top_rebar= Rebar(5)
bottom_rebar = Rebar(5)
stirrup_rebar = Rebar(3)
concrete = Concrete(28)
steel = Steel(420)
reinforcement = ReinforcementProperties(2,2,top_rebar,bottom_rebar,2, stirrup_rebar)
geometry = Rectangular(0.3,0.4,5)
beam = Beam(geometry, 0.04, concrete,steel, reinforcement)



if __name__ == '__main__':
    print (beam)
    #print(beam.rebar.top_rebar_diameter, beam.rebar.top_rebar_area*10000, beam.top_effective_height, beam.simple_top_nominal_moment_strenght, beam.simple_bottom_nominal_moment_strenght, beam.nominal_shear_strenght)