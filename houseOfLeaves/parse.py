with open("./data.txt", "r") as file:
    data = [word[0] for word in file.read().split(" ")]
    print("".join(data))
