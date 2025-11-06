import matplotlib.pyplot as plt

data = [1,2,2,3,3,3,4,4,4,4,5,5,6,6,7]

plt.hist(data,bins=5,edgecolor='black')

plt.xlabel("value")
plt.ylabel("frequency")
plt.title("simple hisorigram graph")

plt.show()
