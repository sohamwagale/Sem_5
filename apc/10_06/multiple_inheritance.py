class Car:
    def __init__(self,make,model,year):
        self.make = make
        self.model = model
        self.year = year

    def start_engine(self):
        print("---THE ENGINE IS NOW RUNNING----")
   
    def stop_engine(self):
        print("---THE ENGINE HAS BEEN TURNED OFF---")

class ElectricCar(Car):
    def __init__(self,make,model,year,battery_capacity):
        super.__init__(make,model,year)
        self.battery_capacity = battery_capacity

    def charge_battery(self):
        print("Charging the Battery....")

    def check_battery_status(self):
        print("Battery Status is 60%")

class SportsCar(Car):
    def __init__(self,make,model,year,horse_power,top_speed):
        super().__init__(make,model,year)
        self.horse_power = horse_power
        self.top_speed = top_speed

    def accelerate(self):
        print("Accelerating to the top speed....")

    def brake(self):
        print("Slowing Down")

class ElectricSportsCar(ElectricCar,SportsCar):
    def __init__(self,make,model,year,battery_capacity,horse_power,top_speed):
        ElectricCar.__init__(self,make,model,year,battery_capacity)
        SportsCar.__init__(self,make,model,year,horse_power,top_speed)

    def display_info(self):
        print(f"{self.year} {self.make} {self.model}")
        print(f"horse Power: {self.horse_power} hp")
        print(f"Top speed: {self.top_speed} km/h")
        print(f"Battery Capacity: {self.battery_capacity} kwh")

my_car = ElectricSportsCar("Tesla", "Roadster",2023,100,1000,390)

my_car.display_info()
