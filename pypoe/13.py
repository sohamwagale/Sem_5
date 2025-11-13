# program for Single inheritance

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


human = LivingThing(78,"Vertebrate")
human.mas()
human.type()
