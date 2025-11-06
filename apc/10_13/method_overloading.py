class Calculator:
    def add(self, a=None, b=None, c=None):
        if a is not None and b is not None and c is not None:
            print("Sum of three:", a + b + c)
        elif a is not None and b is not None:
            print("Sum of two:", a + b)
        else:
            print("Invalid input")

obj = Calculator()
obj.add(5, 10)      
obj.add(5, 10, 15)   
