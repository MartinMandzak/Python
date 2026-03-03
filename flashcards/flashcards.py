import doc_reader
import pandas as pd
import random

data = doc_reader.read_all_in_dir('./data/')
# data= doc_reader.read_file('./data/Slovicka_NJ_1__2_.docx')

n_of_questions = 10
total = 0

for i in range(n_of_questions):
    # pick random row then random col
    row = random.randint(0,len(data))
    col = random.randint(0,1)
    print(f"Word {i+1}\n{data.iloc[row, col]}")
    answer = list(map(str, input('? ')))

    if answer == data.iloc[row, abs(col-1)]:
        print("Correct!")
        total+=1
    else:
        print(f"Incorrect! Should have been '{data.iloc[row, abs(col-1)]}' \nfrom:[{data.iloc[row, 2]}]\n")
 
print(f"Total score: {total}/{n_of_questions}")

