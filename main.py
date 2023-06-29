from classes import BeamSection, Rebar, Reinforcement, Rectangular, Concrete, Steel, TransverseRebar, ReinforcementLocationType

top_rebar= Reinforcement(2,Rebar(5),ReinforcementLocationType.TOP)
bottom_rebar= Reinforcement(2,Rebar(5),ReinforcementLocationType.BOTTOM)
stirrup_rebar = Reinforcement(2,TransverseRebar(3, 0.2),ReinforcementLocationType.TRANSVERSE)
concrete = Concrete(28, EC_factor=4700)
steel = Steel(420)
geometry = Rectangular(0.2,0.3)
beam = BeamSection("id")
beam.set_concrete(concrete)
beam.set_cover(0.04)
beam.set_reinforcement(top_rebar)
beam.set_reinforcement(bottom_rebar)
beam.set_reinforcement(stirrup_rebar)
beam.set_steel(steel)
beam.set_section(geometry)
# beam.set_aditional_reinforcement(Reinforcement(1,Rebar(8),ReinforcementLocationType.TOP))
# beam.set_aditional_reinforcement(Reinforcement(1,Rebar(10),ReinforcementLocationType.TOP))




if __name__ == '__main__':
#     print(beam.cross_section.__dict__())
    print(beam.__dict__())
#     for key,value in beam.__dict__().items():
#             print(key,value)
    # print(beam.top_lambda_delta)
    # print(beam.top_deflexion_multiplier(100))
    # beam.set_aditional_reinforcement(Reinforcement(1,Rebar(8),ReinforcementLocationType.TOP))
    # beam.set_aditional_reinforcement(Reinforcement(1,Rebar(10),ReinforcementLocationType.TOP))
    # print(beam)
    # print(beam.reinforcement_dict["TOP"]["bar_diameters"],beam.reinforcement_dict["TOP"]["bar_area"], beam.top_flexural_ro, beam.top_effective_height, sep="\n")
    # print(beam.top_lambda_delta)
    # print(beam.top_deflexion_multiplier(100))
    # print(beam.minimum_reinforcement_ratio())
    # print(beam.minimum_bottom_area(), beam.minimum_reinforcement_ratio())

    # top_rebar= Reinforcement(5,Rebar(5),ReinforcementLocationType.TOP)
    # beam.get_reinforcement(top_rebar)
    # print(beam)
