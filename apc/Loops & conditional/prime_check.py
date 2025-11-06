num = int(input("Enter a Number for Prime Check: "))

if num <= 1:
    print(f"{num} is not a prime number.")
else:
    is_prime = True
    for i in range(2,num):
        if num % i == 0:
            is_prime =False
            break
    if is_prime:
        print(num, "is a prime number")
    else:
        print(num, "is not a prime number")
