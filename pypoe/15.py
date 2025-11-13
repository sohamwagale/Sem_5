# program for demonstrating any 5 functions of Array 


import array as arr

a = arr.array('i',[1,45,435,34,654,876,453,32])


print("The Original array : ",a)

a.append(32)
print("Array after append : ",a)

cnt = a.count()
print("Count of the elements in the Array : ",cnt)

a.extend([76,56,45])
print("The array after extend function : ", a)

a.insert(0,54354)
print("The array after inserting 54354 at position 0 ",a)

index = a.index(45)
print("The index of the first occurence of 45 in the array",index)