str1 = 'Linus Torvald'
print("string using single quotes: "+str1)

str2 = "Linus Torvald"
print("string using double quotes: "+str2)

str3 = """string using triple quotes:
        Linus Torvald is created Linux
                as a Hobby Project"""

print(str3)

print("-------printing string using for loop-------")
for char in str3:
    print(char,end='')
print()


new_str = str1.upper()
print("UpperCase str1: "+ new_str)

if(str1.islower()):
    print("str1 is lower")
else:
    print("str1 is upper")


print("-------Slicing------------")

main_str = "UNIX is mother of all OS"
print(main_str)
print("Length of the string is: ", len(main_str))

print(main_str[:22])
print(main_str[::-1])
print(main_str[-1:-11:-1])
