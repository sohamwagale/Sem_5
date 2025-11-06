def largest_of_n_numbers(numbers,n):
    largest_number = numbers[0]
    for number in numbers:
        if number > largest_number:
            largest_number = number

    return largest_number

    
n = int(input("How Many Numbers you are taking as Input: "))
print("Enter Numbers in list")

i = 0
numbers = list()
while(i < n):
    temp = int(input("list[{}]: ".format(i)))
    numbers.insert(i,temp)
    i += 1

large = largest_of_n_numbers(numbers,n)
print(f"largest number is {large}")
