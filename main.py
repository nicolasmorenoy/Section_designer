from classes import Beam, RebarProperties, ReinforcementProperties, Rectangular

top_rebar= RebarProperties(5)
bottom_rebar = RebarProperties(5)
stirrup_rebar = RebarProperties(3)
reinforcement = ReinforcementProperties(2,2,top_rebar,bottom_rebar,stirrup_rebar,2)
geometry = Rectangular(0.3,0.4,5)
beam = Beam(geometry,0.04,28,420, reinforcement)



if __name__ == '__main__':
    print(beam.rebar.top_rebar_diameter, beam.rebar.top_rebar_area*10000)