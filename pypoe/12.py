# program for Method overriding 

class Animals:

    def __init__(self, name):
        self.name = name

    def give_birth(self):
        print(self.name," may lay eggs or Direct birth")

class Mammals(Animals):
    def give_birth(self):
        print(self.name," give direct birth")

class NonMammals(Animals):
    def give_birth(self):
        print(self.name, " give eggs")

animal = Animals("Animal")
animal.give_birth()

human = Mammals("Humans")
human.give_birth()

hen = NonMammals("Hen")
hen.give_birth()