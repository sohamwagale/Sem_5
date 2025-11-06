class Vehicle:
    def __init__(self,wheels):
        self.wheels = wheels
        print("PARENT CONSTRUCTOR CALLED!")

    def show(self):
        print(f"wheels: {self.wheels}")

class Car(Vehicle):
    def __init__(self,name,wheels):
        super().__init__(wheels)
        self.name = name
        print("CHILD CONSTRUCOR CALLED!")

    def show(self):
        super().show()
        print(f"name: {self.name}, wheels: {self.wheels}")

car = Car("Skoda Rapid",4)
car.show()
