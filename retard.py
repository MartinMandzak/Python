import matplotlib.pyplot as mpl
import pandas as pd
import csv

keys = ['bed', 'lamp', 'spasm', 'wardrobe', 'backpack', 'left', 'belt']

def new():
    with open("./retard.csv", "w") as file:
        for key in keys:
            file.write(key)
            if keys.index(key) != len(keys)-1: file.write(',')

def question():
    question_bank = ['stood up and sat down on his bed ','turned his lamp on and off ', 'had a spasm on his bed ', 'opened his wardrobe ', 'fucked with his backpack ', 'leave the room ', 'fucked with his belt ']
    with open("./retard.csv", "a") as file:
        print("How many times did he: ")
        for question in question_bank:
            answer = str(input(question))
            file.write(answer)
            if question_bank.index(question) != len(question_bank)-1: file.write(',')

def load():
    with open("./retard.csv", newline='') as file:
        read_data = []
        retard_watcher = csv.reader(file, delimiter = ',')

        for row in retard_watcher:
            read_data.append(row)
            print(row)

        return np.array(read_data)

def chart():
    data = pd.read_csv('./retard.csv')
    
    for column in data.columns:
        mpl.plot(data.index+1, data[column], marker='o', linestyle='-', label = column)
    mpl.xlabel("Days")
    mpl.ylabel("Amt. of times")
    mpl.title("Retard-o-meter")

    mpl.legend()
    mpl.grid(True)
    mpl.show()

chart()
