n = int(input("Enter Limit for printing ODD numbers: "))

print("-------------------Odd Number up to {}------------------".format(n))
i = 0
while(i < n):
    if(i % 2 != 0):
        print(i)
    i += 1
