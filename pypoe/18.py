# program for demonstrating any 5 functions of string

s = 'Hello World'
print("The original string : ",s)

sr = s.replace("Hello","Hola")
print("The returned value after s.replace(old,new): ",sr)

isalnum = s.isalnum()
print("Is the string a alphabet or number : ",isalnum)

cap = s.capitalize()
print("Capitalized version of the string : ",cap)

world = s.endswith("World")
print("Does the string end with world : ",world)

wind = s.find("W")
print("The position of W is : ",wind)
