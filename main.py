from classes import Beam, RebarProperties, ReinforcementProperties, Rectangular, Concrete, Steel

top_rebar= RebarProperties(5)
bottom_rebar = RebarProperties(5)
stirrup_rebar = RebarProperties(3)
concrete = Concrete(28)
steel = Steel(420)
reinforcement = ReinforcementProperties(2,2,top_rebar,bottom_rebar,stirrup_rebar,2)
geometry = Rectangular(0.3,0.4,5)
beam = Beam(geometry, 0.04, concrete,steel, reinforcement, 0.2)



if __name__ == '__main__':
    print(beam.rebar.top_rebar_diameter, beam.rebar.top_rebar_area*10000, beam.top_effective_height, beam.simple_top_nominal_moment_strenght, beam.simple_bottom_nominal_moment_strenght, beam.nominal_shear_strenght)