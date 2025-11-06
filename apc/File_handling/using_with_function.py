#using with function
with open("/etc/passwd","r") as file:
    content = file.read()
    print(content,end="")
    
