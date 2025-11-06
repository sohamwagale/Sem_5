def print_design(n):
    for i in range(n):
        for j in range(1,i + 2):
            print(j,end=' ')
        print()

n = int(input("Enter N: "))
print_design(n)
