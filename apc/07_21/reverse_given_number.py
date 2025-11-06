num = int(input("Enter a number for Reverse: "))

original_num = num

reverse = 0
while num > 0:
    digit = num % 10
    reverse = reverse * 10 + digit
    num //= 10

print(f"reverse of {original_num} is {reverse}")
