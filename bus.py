import random

class Bus:
    bus_id,capacity,stops,passengers = "null",-1,-1,0 # -1 are just dummy values
    def __init__(self,bus_id,capacity, stops):
        self.bus_id,self.capacity, self.stops = bus_id,capacity,stops

#####

bus_station = [Bus("A123",50,10), Bus("B456",25,5), Bus("C789",75,15)]

for bus in bus_station:
    print(f"-- Bus {bus.bus_id} --")
    for stop in range(bus.stops):
        p = random.randint(-bus.passengers, bus.capacity - bus.passengers)
        bus.passengers += p
        print(f"Stop no. {stop+1} -> Passengers: {bus.passengers}/{bus.capacity} => {p}")
    print(f"{bus.passengers} people left at the last stop.")
    print("##################")

