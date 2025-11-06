import pandas as pd

print("pd.Series() Example:")
s = pd.Series([10, 20, 30, 40])
print(s, "\n")

print("pd.DataFrame() Example:")
data = {"Name": ["Alice", "Bob", "Charlie"], "Age": [25, 30, 35]}
df = pd.DataFrame(data)
print(df, "\n")

print("df.head() Example:")
print(df.head(2), "\n")

print("df.info() Example:")
print(df.info(), "\n")

print("df.describe() Example:")
print(df.describe(), "\n")

print("df.loc[] and df.iloc[] Example:")
print("Row with label 1 using loc:\n", df.loc[1])
print("Element at row 0, col 1 using iloc:", df.iloc[0, 1], "\n")

print("df.drop() Example:")
df2 = df.drop("Age", axis=1)
print(df2, "\n")

print("Add New Column Example:")
df["Salary"] = [50000, 60000, 70000]
print(df, "\n")

print("df.sort_values() Example:")
sorted_df = df.sort_values(by="Age", ascending=False)
print(sorted_df, "\n")

print("df.groupby() Example:")
data2 = {"Department": ["IT", "HR", "IT", "Finance", "HR"], "Salary": [60000, 55000, 75000, 80000, 50000]}
df_group = pd.DataFrame(data2)
grouped = df_group.groupby("Department")["Salary"].mean()
print(grouped, "\n")