try:
    print("---Addition of Two Numbers-----")
    no1 = int(input("Enter the first no:"))
    no2 = int(input("Enter the second no:"))
    result = no1/no2
    print("result is: ",result)
except ZeroDivisionError:
    print("Division by zero is NOT allowed")

