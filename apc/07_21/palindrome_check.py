num = int(input("Enter a number for Palindrome Check: "))

original_num = num

reverse = 0
while num > 0:
    digit = num % 10
    reverse = reverse * 10 + digit
    num //=10

if original_num == reverse:
    print(original_num, "is a plindrome number")
else:
    print(original_num, "isn't a palindrome number")
