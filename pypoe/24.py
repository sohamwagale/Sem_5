# program for use of Numpy library

import numpy as np

a = np.array([42,45,67,98,765,43,2])
print(a[4])

a2 = np.array([[3,2,4],[7,6,4],[2,8,5]])
print(a2[2,2])

a3 = np.array([[[1,2],[4,3]],[[6,3],[3,7]]])
print(a3[1,0,1])

rand = np.random.randint(54)
print("Random number is : ",rand)

np.save('files/arr.npy',a3)
print("Array saved as arr.npy file  ")

arr = np.array([4, 8, 15, 16, 23, 42])
print("Original array :", arr)

# 1. reshape()
reshaped = arr.reshape(2, 3)
print("Array after reshape(2,3):")
print(reshaped)

# 2. mean()
print("Mean of array:", np.mean(arr))

# 3. max()
print("Maximum value in array:", np.max(arr))

# 4. sort()
sorted_arr = np.sort(arr)
print("Sorted array:", sorted_arr)

# 5. sum()
print("Sum of all elements:", np.sum(arr))
