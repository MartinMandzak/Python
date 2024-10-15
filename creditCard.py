import random
from datetime import datetime
cards = [(''.join([str(random.randint(0,9)) for num in range (19)]), str(random.randint(1,12))+'/'+str(datetime.now().year+random.randint(0,3))[2:]) for card in range(10)]
print([(card[0][:16]+' CVV: '+card[0][16:],'Exp. Date: '+card[1]) for card in cards])

