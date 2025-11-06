import matplotlib.pyplot as plt

categories = ['A','B','C','D','E']
values = [5,8,11,4,6]

plt.bar(categories,values)

plt.xlabel('Categories')
plt.ylabel('Values')
plt.title("BAR GRAPH")
plt.savefig("bb.png")
plt.show()
