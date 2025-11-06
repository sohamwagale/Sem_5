with open("new.txt","a+") as dest_file:
    with open("/etc/group","r") as src_file:
        content = src_file.read()
        dest_file.write(content)

print("----DATA APPENDED SUCCESSFULLY---")
