print([x**2 for x in range(100) if (lambda x: x % 2 == 0)(x)]) 
