# program to read the contents from a one file and write into another file 
 
contents = ''

with open("files/5_one.txt" , 'r') as f1:
    contents = f1.read()

with open("files/5_two.txt" , 'w') as f2:
    f2.write(contents)
    print("Content written :" , contents)

