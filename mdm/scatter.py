import matplotlib.pyplot as plt

# Data
study_hours = [1, 2, 3, 4, 5, 6, 7, 8]
marks = [35, 40, 50, 55, 60, 70, 75, 85]

# Plot
plt.scatter(study_hours, marks, color='red')

# Labels and Title
plt.title("Study Time vs Marks Scored")
plt.xlabel("Study Hours")
plt.ylabel("Marks Scored")

# Show
plt.show()
