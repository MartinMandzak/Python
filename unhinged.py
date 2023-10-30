"""
God is dead. And we killed him.
"""
with open("./coords.txt","r") as file: data = [tuple(int(xy) for xy in line.split(',')) for line in file.readlines()];road=[((data[i][0]-data[i+1][0])**2+(data[i][1]-data[i+1][1])**2)**0.5 for i in range(len(data)-1)];prox=[((150-data[i][0])**2+(100-data[i][1])**2)**0.5 for i in range(len(data)-1)];print(f"total: {round(sum(road),2)} km and closest to tower was on the {prox.index(min(prox))}th day ({round(min(prox),2)} km) ")
