n = int(input("Enter limit for sum of Even numbers: "))

i = 0
result = 0
while(i < n):
    if(i % 2 == 0):
        result += i
    i += 1

print(f"Sum of Even numbers upto {n} is {result}")
