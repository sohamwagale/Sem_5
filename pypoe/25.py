# program for use of pandas library

import pandas as pd

data = {
    "Name": ["Soham", "Aarav", "Mira", "Riya"],
    "Age": [21, 19, 23, 20],
    "Marks": [88, 92, 79, 95]
}

df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)

# 1. head()
print("\nFirst 2 rows using head():")
print(df.head(2))

# 2. describe()
print("\nStatistical summary using describe():")
print(df.describe())

# 3. sort_values()
print("\nSorting by Marks:")
print(df.sort_values("Marks"))

# 4. loc[]
print("\nSelecting row using loc:")
print(df.loc[2])

# 5. drop()
print("\nDropping the column 'Marks':")
print(df.drop("Marks", axis=1))
