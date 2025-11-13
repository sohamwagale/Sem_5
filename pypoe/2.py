# Find the factorial of a number in python. 

num = int(input("Enter a number: "))

fact = 1
for i in range(num,0,-1):
    fact*=i

print("The factorial is " ,fact)