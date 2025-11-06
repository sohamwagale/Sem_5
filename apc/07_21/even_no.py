x = int(input("Enter Limit for printing Even numbers: "))

print("----------------Even numbers up to {}---------------------".format(x))
i = 0
while(i < x):
    if(i % 2 == 0):
        print(i)
    i += 1
