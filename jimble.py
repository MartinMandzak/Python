import random

turns = random.randint(1,6)
win_condition = random.randint(0,100)
turn_print = turns + 1

symbols = ['🔵', '🟤', '🟡', '⚪', '🟢']
weights = [0.25, 0.25, 0.2, 0.25, 0.05]

if win_condition <= 15: turn_print = 'X'; turns = 6

n = str(input("What's today's Jimble number? "))
print(f" Jimble {n} {turn_print}/7*")
for turn in range(turns):
    line = random.choices(symbols, weights = weights, k=6)
    print(''.join(line))

if win_condition > 15:
    print('⚪⚪⚪⚪⚪⚪')
else:
    print(''.join(random.choices(symbols, weights = weights, k=6)))
