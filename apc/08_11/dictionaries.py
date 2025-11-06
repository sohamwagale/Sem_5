student = {"name":"Abhijeet","roll_no":41,"Rank":4}
print(student)

student.update({"ph no":523234523})
print(student)

print("name of the student is: ",student.get("name"))
del student["roll_no"]
print("after deletining students roll:",student)

student["name"]= "Parth"
print("after chaning name:",student)