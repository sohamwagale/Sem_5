def smallest_of_n_numbers(numbers,n):
    smallest_number = numbers[0]
    for number in numbers:
        if(number < smallest_number):
            smallest_number = number

    return smallest_number


n = int(input("How many number you're taking as a Input: "))
print("Enter Numbers in list")

numbers = list()
i = 0
while(i < n):
    temp = int(input("list[{}]: ".format(i)))
    numbers.insert(i,temp)
    i += 1

smallest_number = smallest_of_n_numbers(numbers,n)
print(f"smallest number is {smallest_number}")
