class Car:
    def __init__(self,make,model,year):
        self.make = make
        self.model = model
        self.year = year

    def describe(self):
        return f"{self.year} {self.model} {self.make}"
    
my_car1 = Car("Toyota","Fortuner",2021)
my_car2 = Car("Mahendra","XUV",2020)

print(my_car1.describe())
print(my_car2.describe())
