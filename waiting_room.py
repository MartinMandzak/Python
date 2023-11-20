"""
An exercise based on FIFO
"""
waiting_room = []
while True:
    x = str(input(': '))
    match x:
        case "next":
            waiting_room.pop(0) # LIFO if idx = -1
        case "end":
            break
        case _:
            waiting_room.append(x)
    print(waiting_room)
