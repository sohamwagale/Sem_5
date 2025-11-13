# program to read the contents from a file and display on console 

import os

file_contents = ''

with open("files/4.txt" , "r") as fl:
    file_contents = fl.read()

print(file_contents)