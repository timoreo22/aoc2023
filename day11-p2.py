f = open("day11-input.txt")
lines: list[str] = [data.strip() for data in f.readlines() if len(data.strip()) > 0]
f.close()

galaxy = set()
colexp = set()
linexp = set()
for x in range(len(lines)):
    # Find S
    for y in range(len(lines[x])):
        if lines[x][y] == '#':
            galaxy.add((x, y))
            linexp.add(x)
            colexp.add(y)  # add col to no-expansion list

linesexp = list(set(range(len(lines))).difference(linexp))
linesexp.sort()
colsexp = list(set(range(len(lines[0]))).difference(colexp))
colsexp.sort()
del colexp
del linexp
print(galaxy)
# expand universe
galaxyEx = set()
for g in galaxy:
    expx = 0
    expy = 0
    for lidx in linesexp:
        if lidx < g[0]:
            expx += 999999
    for cidx in colsexp:
        if cidx < g[1]:
            expy += 999999
    galaxyEx.add((g[0] + expx, g[1] + expy))
print(galaxyEx)


def manhattan(current_cell, goal):
    return abs(current_cell[0] - goal[0]) + abs(current_cell[1] - goal[1])


def reach():
    nodes = galaxyEx.copy()
    total = 0
    while nodes:
        n = nodes.pop()
        for other in nodes:
            # print(n, "to", other, "=", len(path), "(found in ops)", runs)
            total += manhattan(n, other)
    print("total is", total)


reach()
