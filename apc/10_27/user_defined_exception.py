class NegativeNumberException(Exception):
    pass
try:
    n = int(input("Enter the number"))
    if n < 0:
        raise NegativeNumberException("Negative Number isn't Allowded!")
    print("Your entered number is:",n)

except NegativeNumberException as e:
    print("Error:",e)
