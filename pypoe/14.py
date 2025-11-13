# program for multilevel inheritance 

class Matter:
    def __init__(self,mass):
        self.mass = mass

    def mas(self):
        print("Mass of this matter is : ",self.mass)

class LivingThing(Matter):

    def __init__(self, mass, classi):
        self.classi = classi
        super().__init__(mass)

    def type(self):
        print("The classification of this living thing is : ",self.classi)


class Human(LivingThing):

    def __init__(self,name, mass, classi):
        super().__init__(mass, classi)
        self.name = name

    def nam(self):
        print("Name of this human is : ",self.name)


soham = Human("Soham Wagale", 78, "Vertebrate")
soham.mas()
soham.type()
soham.nam()


