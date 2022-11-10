from classes import Beam, Rebar, Reinforcement, Rectangular, Concrete, Steel, TransverseRebar

top_rebar= Reinforcement(2,Rebar(5))
bottom_rebar = Reinforcement(2,Rebar(5))
stirrup_rebar = Reinforcement(2,TransverseRebar(3, 0.2))
concrete = Concrete(28, EC_factor=3900)
steel = Steel(420)
geometry = Rectangular(0.4,0.4)
beam = Beam(geometry, 5, 0.04, concrete,steel, top_rebar, bottom_rebar, stirrup_rebar)



if __name__ == '__main__':
    print(beam)
