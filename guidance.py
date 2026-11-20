from Spaceship import Space_ship
from Lunar_Environment import Lunar_Environment
import math
class Guidance:
    def __init__(self):
        self.space_ship = Space_ship()
        self.lunar = Lunar_Environment()
        self.dt = 0.02
        self.thrust_max = 2.1*(self.space_ship.curr_mass * self.lunar.gravity)

    def simulation(self):
        n = 0
        while self.space_ship.altitude > 0:
            #gonna use V^2= Vo^2 + 2achange in x
            new_a = ((self.space_ship.velocity)**2)/(2*self.space_ship.altitude)
            self.space_ship.thrust = ((self.space_ship.curr_mass * self.lunar.gravity)+(self.space_ship.curr_mass*new_a))
            mass_flow_rate = (self.space_ship.thrust/(self.space_ship.isp * 9.80665))
            self.space_ship.calc_acceleration(self.lunar.gravity)
            self.space_ship.update_flight_comp(self.dt, mass_flow_rate)
            if n%10 == 0:
                print(f"new spaceship thrust {self.space_ship.thrust}, new altitude {self.space_ship.altitude}, new velocity {self.space_ship.velocity}, new acceleration {self.space_ship.acceleration}")
            n+=1
            if self.space_ship.altitude < 1.7 and abs(self.space_ship.velocity)<1:
                self.space_ship.thrust = 0
                break

        impact_speed = math.sqrt((self.space_ship.velocity)**2 + (2*self.lunar.gravity*self.space_ship.altitude))
        if impact_speed < 3.05:
            print("succesfully landed")
            print(impact_speed)
            print(f"new spaceship thrust {self.space_ship.thrust}, new altitude {self.space_ship.altitude}, new velocity {self.space_ship.velocity}, new acceleration {self.space_ship.acceleration}")
        else:
            print("crashed")

guide = Guidance()
guide.simulation()
            
