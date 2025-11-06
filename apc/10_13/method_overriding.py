class Vehicle:
    def start(self):
        print("Vehicle starts........")

class Truck(Vehicle):
    def start(self):
        print("Truck starts......")

truck = Truck()
truck.start()
