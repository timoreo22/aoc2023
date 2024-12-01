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
        total.append(subl)
    # full array built, go back up
    print(total)
    sub_total = 0
    for i in range(len(total) - 1, -1, -1):
        sub_total = total[i][0] - sub_total
        print(sub_total)
    total_value += sub_total
print("result", total_value)
