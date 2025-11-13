# Find factorial of a number using recursion in python

num = int(input("Enter a number: "))

def fact(n):
    if n == 1 : return 1
    else: return n*fact(n-1)

fact = fact(num)
print("The factorial is ",fact)