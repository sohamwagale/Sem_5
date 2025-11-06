n = int(input("Enter limit for printing sum: "))

result = 0
i = 1
while(i < n):
    result += i
    i += 1

print(f"Sum of natural no up to {n} is {result}")
