x = int(input("Enter first no: "))
y = int(input("Enter second no: "))
z = int(input("Enter third no: "))

if(x < y and x < z):
    print(f"{x} is the smaller")
elif(y < x and y < z):
    print(f"{y} is the smaller")
elif(z < x and z < y):
    print(f"{z} is the smaller")
else:
    print("Error (JUST KIDDING)")
