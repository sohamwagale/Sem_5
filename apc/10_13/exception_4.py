try:
    no1 = int(input("Enter the first no: "))
    no2 = int(input("Enter the second no: "))
    result = no1/no2
    print("result:",result)
except ZeroDivisionError:
    print("Division by Zero isn't alloweded")
finally:
    print("--THIS BLOCK ALWAYS EXECUTES--")
