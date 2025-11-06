import matplotlib.pyplot as plt

cat = [ 'Breakfast', 'Lunch','Dinner','dbfdc']
vals = [ 21,43,53,22]


plt.pie(vals,labels=cat,autopct="%1.1f%%")
plt.show()