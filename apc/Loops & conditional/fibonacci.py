n = int(input("Enter N for fibonacci sequence: "))

a = 0
b = 1
i = 0

print("Fibonacci Sequence: ")
while(i < n):
    print(a, end=' ')
    c = a + b
    a = b
    b = c
    i += 1
print()
