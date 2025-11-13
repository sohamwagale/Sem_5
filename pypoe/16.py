# program for demonstrating any 5 functions of list 

ls = [534,32,546,87,54,23,67]

print("Original list : ",ls)

ls.sort()
print("List after sorting : ",ls)

ls.append(43)
print("List after appending 43 : ",ls)

ls.extend([432,543,56,75,24,2])
print("List after extending elements : ",ls)

ls.remove(75)
print("List after removing the element 75 : ",ls)

ls.reverse()
print("List after reversing : ",ls)