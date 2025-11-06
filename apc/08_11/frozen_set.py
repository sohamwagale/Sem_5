book_types = frozenset({"comic","Novel","self-help","Educational","biographic","Poems"})
print(book_types)

#adding and removing is not possible
#book_types.add("Research")     -> it isn't valid

#but still we can do operations like we do on sets like union,intersection,difference

whole_numbers = frozenset([0,1,2,3,4,5,6,7])
natrual_numbers = frozenset([1,2,3,4,5,6,7])
integers = frozenset([-3,-2,-1,0,1,2,3])

print("----following sets are made up using frozen set")
print(f"whole_numbers: {whole_numbers}")
print(f"natrual_numbers: {natrual_numbers}")
print(f"integers: {integers}")


print("intersection of whole number and integers: ",whole_numbers.intersection(integers))
print("difference between whole numbers and integers: ",whole_numbers.difference(integers))