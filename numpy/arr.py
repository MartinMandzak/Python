import numpy as np
import pandas as pd

#evens = np.array([x for x in range(0,100) if x % 2 == 0], dtype=np.int32)
#print(evens)

data = pd.read_csv('telecom_customer_churn.csv')


print(data.head())

