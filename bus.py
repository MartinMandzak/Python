import random

class Bus:
    capacity,stops,passengers = -1,-1,0
    def __init__(self,capacity, stops):
        self.capacity, self.stops = capacity,stops
    def move_people(self, n_people):
        if(0<=self.passengers + n_people<=self.capacity):
            self.passengers += n_people

#####

ranges = 10
bus_station = [Bus(50,10), Bus(25,5), Bus(75,15)]

for bus in bus_station:
    for stop in range(bus.stops):
        print(f"Stop no. {stop+1} -> Current passengers: {bus.passengers}")
        n_people = random.randint(-ranges,ranges)
        bus.move_people(n_people)
    print("##################")

