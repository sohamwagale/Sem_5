num = int(input("Enter a number for Multiplication table: "))

print("--------------Multiplication table of {}---------------------".format(num))
for i in range(1,11):
    result = num * i
    print(f"{num} x {i} = {result}")
