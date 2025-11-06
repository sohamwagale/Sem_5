import matplotlib.pyplot as plt

labels = ['A','B','C','D','E']
values = [34,46,39,15,27]

plt.pie(values, labels=labels, autopct='%1.1f%%')

plt.title('Basic Pie Chart')

plt.show()
