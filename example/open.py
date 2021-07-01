

with open("test.txt", "w") as f:
    f.write("test")

with open("test.txt", mode="r") as f:
    print(f.read())

