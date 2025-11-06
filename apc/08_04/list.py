natural_no = [1,3,5,7]
print(natural_no)

#uninitialized list
new_list1 = list()
new_list2 = []

#inserted 2 at position 1
natural_no.insert(1,2)
print(natural_no)

#append 8
natural_no.append(8)
print(natural_no)

#poped data
poped_data = natural_no.pop()
print("poped data is: ",poped_data)

#remove data
natural_no.remove(3)
print(natural_no)

new_list = [4,6,9,10]
natural_no.extend(new_list)
print(natural_no)

temp_list =[12,4321,441,23,6,92,4]
print(temp_list)

new_list2 = sorted(temp_list)
print("Sorted above list: ",new_list2)

print("index of 4 is: ",natural_no.index(4))

whole_numbers = [0,1,2,3,4,5,6,7]
print(whole_numbers)
whole_numbers.reverse()
print(whole_numbers)


