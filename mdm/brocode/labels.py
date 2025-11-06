import matplotlib.pyplot as plt
import numpy as np


x = np.array([2024,2025,2026,2027,2028])
y1 = np.array([20,32,25,54,38])
y2 = np.array([26,42,5,50,33])

plt.title("Class Size", family = 'Arial',
          fontweight = 'bold',
          fontsize = 19)

plt.xlabel( "Year", family = "Arial",
                    fontsize = 4,
                    fontweight = 'bold',
                    color = 'red'                
)

plt.ylabel( "Students", family = 'Arial',
                        fontsize = 5,
                        fontweight = 'bold',
                        color = 'green'
)

plt.tick_params(axis = 'both',colors = 'blue')

plt.subplots_adjust( bottom=0.1 , left=0.1 )

plt.plot(x,y1)
plt.plot(x,y2) 

plt.xticks(x)

plt.show()