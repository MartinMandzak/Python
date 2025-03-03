import random

PROBLEM_COUNT = 10
MAX_SUM = 20

def gen_problem():
    x,y=0,0
    problem = (x,y)
    operation = random.randint(0,1)

    if operation == 1:
        x = random.randint(0,MAX_SUM)
        y = random.randint(0, MAX_SUM - x)
        op = '+'
        problem = tuple(sorted((x,y)))
        check = x+y
    else:
        x = random.randint(0,MAX_SUM)
        y = random.randint(0, x)
        op = '-'
        problem = tuple(sorted((x,y)))
        check = problem[1] - problem[0]


    print(f"{problem[1]} {op} {problem[0]} = ?")
    answer = int(input())
    return check == answer


points=0
for i in range(PROBLEM_COUNT):
    if gen_problem():
        points+=1

print(f" -- Výsledky ---")
print(f"{points}/{PROBLEM_COUNT}")
