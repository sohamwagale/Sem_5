# Python program to display a horizontal bar chart of the popularity of programming languages

import matplotlib.pyplot as plt

languages = ["Java", "Python","PHP","JavaScript","C#","C++"]
popularity = [22.2,17.6,8.8,8,7.7,6.7]

plt.barh(languages,popularity)
plt.title("Popularity of Languages")
plt.savefig('files/7.png')
plt.show()