class Animal:
    def speaks(self):
        return "Animal Speaks"
    
class Dog(Animal):
    def barks(self):
        return "Dog Barks"

class Puppy(Dog):
    def cry(self):
        return "Puppy Cries"
    
puppy = Puppy()
print(puppy.speaks())
print(puppy.barks())
print(puppy.cry())