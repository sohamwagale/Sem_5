# program for creating function and lambda function 

def func():
    print("This is a normal function")

def func_call(fun):
    print("The function caller is initiated ")
    fun()
    print("The function has been called")

func()
func_call(func)

# Lambda function

func_call(lambda : print("This is a lambda function"))
sq = lambda x : x*x
print(sq(5))