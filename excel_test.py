import pandas as pd

frame = pd.read_csv('excel_test_data.csv')
frame.to_excel('data.xlsx', index=False)
