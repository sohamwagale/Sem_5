# Python program to create a pie chart. 

import matplotlib.pyplot as plt

browsers = ["Chrome", "Safari", "Firefox", "Edge", "Others"]
users = [63, 20, 5, 4, 8]

plt.pie(users , labels=browsers,autopct="%1.1f%%",startangle=90)
plt.axis("equal")
plt.title("Browsers used by People")
plt.savefig("files/8.png")
plt.show()
