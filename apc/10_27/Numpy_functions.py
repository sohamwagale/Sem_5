import numpy as np

#creates array
arr = np.array([11,12,13,14,15])
print("array:",arr)

#create array with range
arr = np.arange(0,10,2)
print("array:",arr)

#create array with value zero
zeros = np.zeros((2,3))
print("Zero Array:\n",zeros)

#create array with value one
ones = np.ones((3,2))
print("array of ones:\n",ones)

#reshapes array
arr = np.arange(1,7)
reshaped = arr.reshape(2,3)
print("original:",arr)
print("reshaped:",reshaped)

#Mean of array 

arr = np.array([10,20,30,40,50])
print("Mean:",np.mean(arr))

#sqrt of members
arr = np.array([4,9,16,64])
print("sprt:",np.sqrt(arr))

#addition of two arrays
arr1 = np.array([111,222,333,444])
arr2 = np.array([1,2,3,4])
print("add: ",np.add(arr1,arr2))

#dot product of two D arrays
A = np.array([[1,2],[3,4]])
B = np.array([[5,6],[7,8]])
print("dot: ",np.dot(A,B))

#min max 
arr = np.array([5,23,69,93,102,4])
print("Max: ",np.max(arr))
print("Min: ",np.min(arr))


