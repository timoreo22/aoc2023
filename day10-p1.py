import numpy as np

f = open("day10-input.txt")
lines: list[str] = f.readlines()
f.close()
factors: dict[str, list[tuple[int, int]]] = {'S': [(1, 0), (-1, 0), (0, 1), (0, -1)],
                                             '|': [(-1, 0), (1, 0)],
                                             '-': [(0, -1), (0, 1)],
                                             'L': [(-1, 0), (0, 1)],
                                             'J': [(-1, 0), (0, -1)],
                                             '7': [(1, 0), (0, -1)],
                                             'F': [(1, 0), (0, 1)],
                                             '.': []
                                             }


def get_indexes(pos: tuple[int, int]) -> list[tuple[int, int]]:
    ret = []
    print(pos, lines[pos[0]][pos[1]])
    for p in factors[lines[pos[0]][pos[1]]]:
        if lines[pos[0] + p[0]][pos[1] + p[1]] in factors:
            ret.append((pos[0] + p[0], pos[1] + p[1]))
    return ret
def get_graph(pos: tuple[int, int]):
    sides = get_indexes(pos)
    g = []
    previous = []
    current = []
    # initial check, remove invalid sides
    for p in sides:
        if pos in get_indexes(p):
            g.append(1)
            previous.append(pos)
            current.append(p)
    print(current)
    while not np.all(current[0] == np.array(current)):
        for idx in range(len(current)):
            indexes = get_indexes(current[idx])
            indexes.remove(previous[idx])
            previous[idx] = current[idx]
            current[idx] = indexes[0]
            g[idx] += 1
    return g[0]


for x in range(len(lines)):
    # Find S
    line = lines[x]
    if 'S' in line:
        print(get_graph((x, line.index('S'))))
