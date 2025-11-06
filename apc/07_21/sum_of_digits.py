num = int(input("Enter number for addition of their digits: "))

result = 0
while num > 0:
    digit = num % 10
    result += digit
    num //= 10

print(f"sum of the digits of the {num} is {result}")

