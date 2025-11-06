def print_design(n):
    for i in range(0,n):
        for j in range(0,i + 1):
            print(chr(ord("A")+j),end=' ')
        print()

n = int(input("Enter n for printing Design: "))
print_design(n)
