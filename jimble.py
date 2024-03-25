import random

turns = random.randint(1,6) # 7th is always all white

symbols = ['🔵', '🟤', '🟡', '⚪', '🟢']
weights = [0.25, 0.25, 0.2, 0.25, 0.05]

n = str(input("What's today's Jimble number? "))
print(f" Jimble {n} {turns+1}/7*")
for turn in range(turns):
    line = random.choices(symbols, weights = weights, k=6)
    print(''.join(line))

print('⚪⚪⚪⚪⚪⚪')
