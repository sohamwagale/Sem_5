import matplotlib.pyplot as plt

x = [1,2,3,4,5]
y = [10,20,25,30,45]

plt.plot(x,y)

plt.grid(which='both', axis='x',linewidth = 3,linestyle='dashdot',color = 'lightgrey')

plt.xticks(x)
plt.xlim(right = 7)
plt.show()

