student = list()
grade = list()

def add_student_and_grade():
    name = str(input("name:"))
    g = float(input("grade:"))
    student.append(name)
    grade.append(g)
    print("--student added successfully---")

def update_grade():
    name = input("enter name of the student to update his/her grade: ")
    if name in student:
        index = student.index(name)
        new_grade = float(input("enter new grade: "))
        grade[index] = new_grade
        print("---Grade updated Successfully----")
    else:
        print("--student isn't in the list----")

def remove_student():
    name = input("enter name of the student to remove from the list: ")
    if name in student:
        index = student.index(name)
        student.pop(index)
        grade.pop(index)
        print("---student removed successfully---")
    else:
        print("---student isn't in the list---")

def avg_grade_of_class():
    if grade:
        avg = sum(grade) / len(grade)
        print("average grade of the class:",avg)
    else:
        print("empty grade list")

def high_and_low_grade():
    if grade:
        print("Highest grade: ",max(grade))
        print("Lowest grade: ",min(grade))
    else:
        print("empty grade list")

while True:
    print("--------student grade system-------")
    print("1->add student")
    print("2->update grade")
    print("3->remove student")
    print("4->avg grade of class")
    print("5->high and low grade")
    print("6->exit")

    response = int(input("Enter your choice(1-6):"))
    if(response == 1):
        add_student_and_grade()
    elif(response == 2):
        update_grade()
    elif(response == 3):
        remove_student()
    elif(response == 4):
        avg_grade_of_class()
    elif(response == 5):
        high_and_low_grade()
    elif(response == 6):
        print("--PROGRAMEE TERMINATED SUCCESSFULLY-----")
        break
    else:
        print("please chose valid option!!")


