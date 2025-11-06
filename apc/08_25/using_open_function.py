file = open("/etc/passwd","r")

print("------------------USING FOR LOOP--------------------")
#using for loop
for data in file:
  print(data,end="")

offset = file.tell()
print(f"The current file offset: {offset}")

file.seek(0,0)  # due to set the position
offset = file.tell()

#using read function
print("-----------------USING READ FUNCTION-------------------")
print(f"After seek function offset is: {offset}")

content = file.read()
print(content)

file.close()
