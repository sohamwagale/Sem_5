# program for demonstrating any 5 functions of dictionary

dic = dict([("Name", "soham"), ("Age", 32)])
print("Original Dict",dic)

dic.update([("Class","TY")])
print("Dict after update",dic)

age = dic.get('Age')
print("Age in dict is : ",age)

dic.pop("Class")
print("Dict after pop('Class')",dic)

keys = dic.keys()
print("Dict after keys()",keys)

dic.clear()
print("Dict after clearing : ",dic)
