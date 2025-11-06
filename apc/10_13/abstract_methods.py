from abc import ABC, abstractmethod

class Shape(ABC):               
    @abstractmethod
    def area(self):
        pass

    def show(self):
        print("This is a shape")

class Rectangle(Shape):
    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth

    def area(self):            
        return self.length * self.breadth


r = Rectangle(10, 5)
r.show()
print("Area of Rectangle:", r.area())
