class Animal:
    def speaks(self):
        return "Animal Speaks"
    
class Dog(Animal):
    def barks(self):
        return "Dog Barks"
    
class Cat(Animal):
    def meow(self):
        return "Cat MEOW"
    
cat = Cat()
dog = Dog()
print(cat.speaks(),cat.meow())
print(dog.speaks(),dog.barks())