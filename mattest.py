import random

n_rounds = 10
correct = 0

for i in range(n_rounds):
    a = random.randint(0,9)
    b = random.randint(0,9)
    user_input = int(input(str(i)+". "+str(a)+"+"+str(b)+ "= ?"))
    if user_input == a+b:
        correct +=1
print(f"Správne si odpovedal na {correct} z {n_rounds} príkladov!")
