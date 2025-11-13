# program for demonstrating any 5 functions of tuple

tup = (32,5,4,534,2,24)
print("Original tuple is : ",tup)

cnt = tup.count()
print("COunt of elements is : ",cnt)

ind = tup.index(534)
print("Index of the element 534 is : ",ind)

clas = tup.__class__()
print("The class of tuple is : ",clas)

ad4 = tup.__add__(4)
print("Tuple after __add__(4)",ad4)

cont2 = tup.__contains__(2)
print("Does the tuple contain the element 2",cont2)
