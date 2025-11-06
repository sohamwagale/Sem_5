c = input("Enter a character: ")

if len(c) == 1:
    c = c.lower()

    if(c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u'):
        print("Entered char is vowel")
    else:
        print("Entered char is consonant")

else:
    print("Please enter Single char")
