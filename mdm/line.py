import matplotlib.pyplot as plt

# Data
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
temperature = [29, 31, 30, 32, 33, 35, 34]

# Plot
plt.plot(days, temperature, color='green', marker='o', linestyle='solid')

# Labels and Title
plt.title("Daily Temperature Over a Week")
plt.xlabel("Days")
plt.ylabel("Temperature (°C)")
plt.grid(True)

# Show
plt.show()
