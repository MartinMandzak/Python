



data=[x for x in list(map(int,input('nums: ').split(' ')))];print(f"{[data[idx] for idx in range(len(data)-1) if [(lambda x,y: x<y)(data[i],data[idx+1]) for i in range(len(data)-1)][idx]]}")


