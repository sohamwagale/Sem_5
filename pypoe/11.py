# Program for method overloading

class Maths:
    
    def add(self,a=None,b=None,c=None):
        if c == None:
            print("Sum is " , a + b)
            return a + b
        
        else: 
            print("Sum is " , a + b + c)
            return a + b + c


math = Maths()
math.add(1,4,5)
math.add(1,4)
