import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib import gridspec

plt.style.use('seaborn-v0_8-darkgrid')

# Create figure layout
fig = plt.figure(figsize=(10, 8))
gs = gridspec.GridSpec(2, 2, figure=fig)

# --- 3D Surface Plot ---
ax1 = fig.add_subplot(gs[0, 0], projection='3d')
X = np.linspace(-5, 5, 100)
Y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))
ax1.plot_surface(X, Y, Z, cmap='viridis')
ax1.set_title("3D Surface")

# --- Line Plot with LaTeX ---
ax2 = fig.add_subplot(gs[0, 1])
x = np.linspace(0, 10, 400)
y = np.sin(x**2)
ax2.plot(x, y, color='r')
ax2.set_title(r"$y = \sin(x^2)$")

# --- Scatter Plot with Color Mapping ---
ax3 = fig.add_subplot(gs[1, 0])
x = np.random.rand(100)
y = np.random.rand(100)
colors = np.sqrt(x**2 + y**2)
ax3.scatter(x, y, c=colors, cmap='plasma')
ax3.set_title("Colored Scatter Plot")

# --- Animated Sine Wave ---
ax4 = fig.add_subplot(gs[1, 1])
x = np.linspace(0, 2*np.pi, 200)
line, = ax4.plot(x, np.sin(x))
ax4.set_ylim(-1.2, 1.2)
ax4.set_title("Animated Sine Wave")

def animate(i):
    line.set_ydata(np.sin(x + i/10))
    return line,

ani = FuncAnimation(fig, animate, frames=100, interval=50, blit=True)

plt.tight_layout()
plt.show()
