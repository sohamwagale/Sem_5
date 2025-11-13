# program to display file available in current directory 

import os

print(os.listdir())
os.chdir("files")
print(os.listdir())