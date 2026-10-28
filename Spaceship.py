from Lunar_Environment import Lunar_Environment
class Space_ship:
    def __init__(self):
        # Mass Compononents
        self.empty_mass = 4214
        self.curr_mass = 10851
        # engine Components
        self.thrust = 0
        self.isp = 311
        self.Nozzle_area = 2734
        self.exit_pressure = 120 #exhaust pressure

        # flight components
        self.acceleration = 0
        self.altitude = 100
        self.velocity = 0
        # Used Apollo Mission metrics  
    
    # Updates numbers real time
    def update_num(self, alt, mass):
        self.curr_mass = mass
        self.altitude = alt

    def calc_thrust(self, e_mass):
        #m.Ve +Ae(Pe) Po is 0 cuz its the moon scratch that
        # use Veq = Isp*go and F/m. = Veq
        #The guidance systems controls the exhaust mass
        #Used Earth gravity because isp of apollo was calculated on earth
        self.thrust = self.isp* e_mass* 9.80665
        print(f"thrust {self.thrust} newtons ")

    def calc_acceleration(self):
        lunar = Lunar_Environment()
        weight = lunar.grav() * self.curr_mass
        net_force = self.thrust- weight
        self.acceleration = net_force/self.curr_mass
        print(f"acceleration {self.acceleration} m/s^2")

space = Space_ship()
space.calc_thrust(14.6)
space.calc_acceleration()


    

    
