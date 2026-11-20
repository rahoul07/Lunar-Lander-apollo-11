from Lunar_Environment import Lunar_Environment
class Space_ship:
    def __init__(self):
        # Mass Compononents
        self.empty_mass = 4214
        self.curr_mass = 15065
        # engine Components
        self.thrust = 0
        self.isp = 311
        self.Nozzle_area = 2734
        self.exit_pressure = 120 #exhaust pressure

        # flight components
        lunar = Lunar_Environment()
        self.acceleration = -lunar.gravity
        self.altitude = 213.4# in meters
        self.velocity = -6.4
        # Used Apollo Mission metrics  

    def calc_thrust(self, e_mass):
        #m.Ve +Ae(Pe) Po is 0 cuz its the moon scratch that
        # use Veq = Isp*go and F/m. = Veq
        #The guidance systems controls the exhaust mass
        #Used Earth gravity because isp of apollo was calculated on earth
        self.thrust = self.isp* e_mass* 9.80665
        print(f"thrust {self.thrust} newtons ")

    def calc_acceleration(self, grav):
        weight = grav * self.curr_mass
        net_force = self.thrust- weight
        self.acceleration = net_force/self.curr_mass

    def update_flight_comp(self, dt, e_mass):
        self.curr_mass = max(self.curr_mass-(e_mass * dt), self.empty_mass)
        self.velocity += self.acceleration * dt
        self.altitude += self.velocity*dt


    

    
