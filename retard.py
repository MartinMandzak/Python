import matplotlib as mpl

keys = ['bed', 'lamp', 'spasm', 'wardrobe', 'backpack', 'left', 'belt']

def new():
    with open("./retard.csv", "w") as file:
        for key in keys:
            file.write(key)
            if keys.index(key) != len(keys)-1: file.write(',')

def question():
    pass

def append(answers): # array
    pass

def load():
    pass

def chart():
    pass

