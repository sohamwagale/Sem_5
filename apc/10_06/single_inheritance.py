class Shape:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def print_measures(self):
        print("Length of the Rectangle is: ",self.x)
        print("Width of the Rectangle is: ",self.y)

class Rectangle(Shape):
    def __init__(self,x,y):
        super().__init__(x,y)

    def calculate_area(self):
        return(self.x * self.y)



rect = Rectangle(10,10)
rect.print_measures()
print("The area of the rectangle is: ",rect.calculate_area())