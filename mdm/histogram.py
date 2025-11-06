import matplotlib.pyplot as plt

# Data
ages = [18, 19, 20, 18, 21, 22, 21, 19, 23, 22, 24, 20, 19, 21, 20]

# Plot
plt.hist(ages, bins=5, color='orange', edgecolor='black')

# Labels and Title
plt.title("Age Distribution of Students")
plt.xlabel("Age")
plt.ylabel("Number of Students")

# Show
plt.show()
