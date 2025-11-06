import matplotlib.pyplot as plt
import numpy as np


x = np.array([2024,2025,2026,2027,2028])
y1 = np.array([20,32,25,54,38])
y2 = np.array([26,42,5,50,33])
y3 = np.array([20,32,22,56,36])

line_style = dict(
    marker = 'v',
    markersize = 10 ,
    markerfacecolor = 'red',
    markeredgecolor = 'green',
    markeredgewidth = 4,
    color = 'blue',
    linewidth = 4,
    linestyle = 'dashdot'
)

plt.plot(x,y1,**line_style)
plt.plot(x,y2,**line_style)
plt.plot(x,y3,**line_style)

plt.show()