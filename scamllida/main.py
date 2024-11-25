import pandas as pd

file_path = 'example.xlsx'

df = pd.read_excel(file_path)
# CRAZY NEW VERSION OF DATA
df_new_version = df.copy(deep=True)
df_new_version["F"] = ["F1", "F2", "F3", "F4", "F5"]


print(df)
print("\n NEW VERSION!!1!!\n")
print(df_new_version)

