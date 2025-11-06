import matplotlib.pyplot as plt

# Data
products = ["Laptops", "Mobiles", "Tablets", "Headphones", "Watches"]
sales = [250, 400, 150, 300, 200]

# Plot
plt.bar(products, sales, color='skyblue')

# Labels and Title
plt.title("Total Sales of Products")
plt.xlabel("Product Category")
plt.ylabel("Sales (in units)")

# Show
plt.show()
