# program for demonstrating any 5 functions of set 

st =  {432,654,15,87,43542,645,76,85,23 }
print("Original set_1",st)
st2 = {432,54,65,674,54,76}
print("Original set_2",st2)


st.update([432,5,654,3,45,34])
print("Set 1 after update : ",st)

st.remove(15)
print("Removes the element 15 : ",st)

st.discard(85) # No error if elem not present
print("The set after discarding the elem 85 : ",st)

st.difference_update(st2)
print("Set 1 after removing all the elems of the Set 2 : ",st)

st.clear()
print("The set 1 after clearing it : ",st)
