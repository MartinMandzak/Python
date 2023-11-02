



data=[x for x in list(map(int,input('nums: ').split(' ')))];print(f"{[data[idx] if [(lambda x,y: x<y)(data[i],data[idx+1]) for i in range(len(data))][idx] else 'kokot' for idx in range(len(data)-1)]}")


