def print_design(n):
    for i in range(0,n):
        for j in range(0,n - i):
            print(chr(ord("A")+ j),end=' ')
        print()

n = int(input("Enter N: "))
print_design(n)
