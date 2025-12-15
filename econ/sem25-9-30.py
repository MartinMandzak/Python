import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_excel("./data/Data Visualization Examples-Exercise.xlsx", sheet_name="Area Chart")
data.set_index("Month", inplace=True)
data.sort_index()

sns.set_theme("notebook")

fig, ax = plt.subplots(figsize=(12,6))

data.plot.area(alpha=0.7, ax=ax)
ax.set_title('Area Chart', fontsize=16)
ax.set_xlabel('Month')
ax.set_ylabel('Values')
ax.legend(title='Series')
plt.tight_layout()
plt.show()

print(data)
