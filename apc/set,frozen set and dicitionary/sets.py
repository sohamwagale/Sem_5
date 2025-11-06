#uninitialized set
books = {}
vendors_of_laptop = set()

natural_numbers = {1,2,3,4,5,6}
print(f"natural_numbers: ",natural_numbers)

natural_numbers.add(11)
print(f"add 11: {natural_numbers}")

natural_numbers.remove(11)
print(f"after Removing 11: {natural_numbers}")

whole_numbers = {0,1,2,3,4,5,6}
print(f"whole numbers: {whole_numbers}")

integers = {-4,-3,-2,-1,0,1,2,3,4}
print("Integers: ",integers)

print("--------Operations on Sets------------")
print("natural_numbers | whole_numbers: ",natural_numbers | whole_numbers)

print("natrual_numbers & whole_numbers: ",natural_numbers & whole_numbers)

print("poped element from natrual numbers: ",natural_numbers.pop())
print("union of whole numers and integers: ",whole_numbers.union(integers))
print("intersection of whole number and integers: ",whole_numbers.intersection(integers))
print("difference between whole numbers and integers: ",whole_numbers.difference(integers))