import numpy as np

f = open("day9-input.txt")
lines = f.readlines()
f.close()
total_value = 0
for line in lines:
    numbers = [int(x) for x in line.split()]
    total = [numbers]
    while np.any(total[len(total) - 1]):
        subl = []
        cl = total[len(total) - 1]
        for i in range(len(cl) - 1):
            subl.append(cl[i + 1] - cl[i])
        print(subl)
        total.append(subl)
    # full array built, go back up
    print(total)
    for i in range(len(total) - 1, -1, -1):
        total_value += total[i][len(total[i])-1]
print(total_value)
