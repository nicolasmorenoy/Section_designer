from classes import Beam, Reinforcement


reinforcement = Reinforcement(2,2,5,5,3,2)
beam = Beam(0.3,0.4,0.04,28,420, reinforcement)



if __name__ == '__main__':
    print(beam.reinforcement_properties)