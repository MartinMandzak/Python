import random
from datetime import datetime
n_cards = 10
cards = [(''.join([str(random.randint(0,9)) for num in range (19)]), str(random.randint(1,12))+'/'+str(datetime.now().year+random.randint(0,3))) for card in range(n_cards)]
print([(card[0][:16]+' CVV: '+card[0][16:],'Exp. Date: '+card[1][:2]+card[1][4:]) for card in cards])

