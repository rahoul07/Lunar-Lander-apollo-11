from Spaceship import Space_ship
from Lunar_Environment import Lunar_Environment
import math

class Guidance:
    def __init__(self):
        self.space_ship = Space_ship()
        self.lunar = Lunar_Environment()
        self.dt = 0.02
        self.max_thrust_rate = 85000
        self.time_lag = 0.075
        self.data_collected = {"time":[0.0],
                               "thrust":[self.space_ship.thrust], 
                               "altitude":[self.space_ship.altitude],
                               "velocity":[self.space_ship.velocity]
                              }
    
        

    def simulation(self):
        n = 0
        while self.space_ship.altitude > 0:
            #gonna use V^2= Vo^2 + 2achange in x
            new_a = ((self.space_ship.velocity)**2)/(2*self.space_ship.altitude) *math.copysign(1, -self.space_ship.velocity)
            thrust_needed = ((self.space_ship.curr_mass * self.lunar.gravity)+(self.space_ship.curr_mass*new_a))
            dr = min((abs(thrust_needed-self.space_ship.thrust))/0.075, (self.max_thrust_rate))
            self.space_ship.thrust = self.space_ship.thrust+(dr*self.dt*(math.copysign(1, (thrust_needed-self.space_ship.thrust))))
            self.data_collected["thrust"].append(self.space_ship.thrust)
            mass_flow_rate = (self.space_ship.thrust/(self.space_ship.isp * 9.80665))
            self.space_ship.calc_acceleration(self.lunar.gravity)
            self.space_ship.update_flight_comp(self.dt, mass_flow_rate)
            new_time = self.data_collected["time"][-1]+self.dt
            self.data_collected["time"].append(new_time)
            self.data_collected["velocity"].append(self.space_ship.velocity)
            self.data_collected["altitude"].append(self.space_ship.altitude)
            if n%10 == 0:
                print(f"new spaceship thrust {self.space_ship.thrust}, new altitude {self.space_ship.altitude}, new velocity {self.space_ship.velocity}, new acceleration {self.space_ship.acceleration}")
            n+=1
            if self.space_ship.altitude < 1.7 and abs(self.space_ship.velocity)<1:
                self.free_fall()
                break
    
        impact_speed = math.sqrt((self.space_ship.velocity)**2 + (2*self.lunar.gravity*self.space_ship.altitude))
        if impact_speed < 3.05:
            new_time = self.data_collected["time"][-1]+self.dt
            self.data_collected["time"].append(new_time)
            self.data_collected["velocity"].append(0)
            self.data_collected["altitude"].append(0)
            self.data_collected["thrust"].append(0)
            print("succesfully landed")
            print(impact_speed)
            print(f"new spaceship thrust {self.space_ship.thrust}, new altitude {self.space_ship.altitude}, new velocity {self.space_ship.velocity}, new acceleration {self.space_ship.acceleration}")
        else:
            print("crashed")
        return self.data_collected

    def free_fall(self):
        self.space_ship.thrust = 0
        #uses the Xf = Xo+Vot -1/2gt^2 formula it has a 1/2 cuz integrating a triangle basically to find distance and the acceleration is constant so its a triangle so its 1/2 bh B = time H = velocity or gt
        # time = (self.space_ship.velocity+math.sqrt((self.space_ship.velocity)**2+(4*(self.lunar.gravity/2)*self.space_ship.altitude)))/self.lunar.gravity
        # i = time/self.dt
        # for x in i: better to use just a while loop
        while self.space_ship.altitude > 0:
            self.data_collected["thrust"].append(self.space_ship.thrust)
            new_time = self.data_collected["time"][-1]+self.dt
            self.data_collected["time"].append(new_time)
            self.space_ship.velocity -= self.lunar.gravity*self.dt
            self.data_collected["velocity"].append(self.space_ship.velocity)
            self.space_ship.altitude += self.space_ship.velocity *self.dt
            self.space_ship.altitude = max(self.space_ship.altitude, 0)
            self.data_collected["altitude"].append(self.space_ship.altitude)

if __name__ == "__main__":
    guide = Guidance()
    guide.simulation()
            
