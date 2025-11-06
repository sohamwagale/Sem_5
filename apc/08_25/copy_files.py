src = open("/etc/passwd","r")
dest = open("new.txt","w+")

for data in src:
    dest.write(data)

print("-----FILE COPIED SUCCESSFULLLY-----")
src.close()
dest.close()
