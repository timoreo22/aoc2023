import functools

import numpy as np
from sys import setrecursionlimit
setrecursionlimit(20000)

f = open("day10-input.txt")
lines: list[str] = [data.strip() for data in f.readlines() if len(data.strip()) > 0]
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


@functools.lru_cache(maxsize=None)
def _get_indexes(pos: tuple[int, int]) -> list[tuple[int, int]]:
    ret = []
    # print(pos, lines[pos[0]][pos[1]])
    for p in factors[lines[pos[0]][pos[1]]]:
        if lines[pos[0] + p[0]][pos[1] + p[1]] in factors:
            ret.append((pos[0] + p[0], pos[1] + p[1]))
    return ret


def get_indexes(pos: tuple[int, int]) -> list[tuple[int, int]]:
    return _get_indexes(pos).copy()


def can_go_to(pos: tuple[int, int], other: tuple[int, int], graph: set[tuple[int, int]]) -> bool:
    if other not in graph:
        return False
    if not is_valid_pos(other):
        return True
    idx = get_indexes(other)
    return pos in idx
    # vect = (other[0]*2 - pos[0], other[1]*2 - pos[1])
    # return pos in idx or vect in idx


# assumes other is part of the loop
def squeeze(pos: tuple[int, int], other: tuple[int, int], side: bool, graph: set[tuple[int, int]]) -> bool:
    vneighbour = get_neighbour(other, pos, side)
    return not can_go_to(other, vneighbour, graph)


def get_neighbour(other, pos, side):
    vect: tuple[int, int] = (other[0] - pos[0], other[1] - pos[1])
    neighbour: tuple[int, int]
    if vect[0] == 0:
        if side:
            neighbour = (1, 0)
        else:
            neighbour = (-1, 0)
    else:
        if side:
            neighbour = (0, 1)
        else:
            neighbour = (0, -1)
    vneighbour = (other[0] + neighbour[0], other[1] + neighbour[1])
    return vneighbour


def is_valid_pos(pos: tuple[int, int]):
    return 0 <= pos[0] < len(lines) and 0 <= pos[1] < len(lines[0])


def mark_on_loop(start_pos: tuple[int, int], marked: set[tuple[int, int]], graph: set[tuple[int, int]]):
    # for start, assuming that every side that isn't graph is outside !
    sides = []
    for x in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ne = (start_pos[0] + x[0], start_pos[1] + x[1])
        if ne not in graph:
            sides.append(x)
    print(sides)
    for x in sides:
        floodfill((start_pos[0] + x[0], start_pos[1] + x[1]), marked, graph)
    previous_pos = start_pos
    current_pos = get_indexes(start_pos)[0]  # pick first, randomly, either works
    print(previous_pos, current_pos)
    vec = (current_pos[0] - previous_pos[0], current_pos[1] - previous_pos[1])
    while current_pos != start_pos:  # stop when fully looped
        indexes = get_indexes(current_pos)
        indexes.remove(previous_pos)
        previous_pos = current_pos
        current_pos = indexes[0]

        nvec = (current_pos[0] - previous_pos[0], current_pos[1] - previous_pos[1])
        if lines[current_pos[0]][current_pos[1]] in ('J', 'L', '7', 'F'):
            i = get_indexes(current_pos)
            i.remove(previous_pos)
            floodfill((current_pos[0] + sides[0][0], current_pos[1] + sides[0][1]), marked, graph)
            if nvec[0] == -1:
                if lines[current_pos[0]][current_pos[1]] == 'J':
                    for sidx in range(len(sides)):
                        sides[sidx] = (sides[sidx][1], sides[sidx][0])
                else:  # L
                    for sidx in range(len(sides)):
                        sides[sidx] = (-sides[sidx][1], -sides[sidx][0])
            elif nvec[0] == 1:
                if lines[current_pos[0]][current_pos[1]] == 'F':
                    for sidx in range(len(sides)):
                        sides[sidx] = (sides[sidx][1], sides[sidx][0])
                else:  # 7
                    for sidx in range(len(sides)):
                        sides[sidx] = (-sides[sidx][1], -sides[sidx][0])
            elif nvec[1] == 1:
                if lines[current_pos[0]][current_pos[1]] == '7':
                    for sidx in range(len(sides)):
                        sides[sidx] = (sides[sidx][1], sides[sidx][0])
                else:  # J
                    for sidx in range(len(sides)):
                        sides[sidx] = (-sides[sidx][1], -sides[sidx][0])
            elif nvec[1] == -1:
                if lines[current_pos[0]][current_pos[1]] == 'L':
                    for sidx in range(len(sides)):
                        sides[sidx] = (sides[sidx][1], sides[sidx][0])
                else:  # F
                    for sidx in range(len(sides)):
                        sides[sidx] = (-sides[sidx][1], -sides[sidx][0])

            floodfill((current_pos[0] + sides[0][0], current_pos[1] + sides[0][1]), marked, graph)
            vec = nvec
        else:
            floodfill((current_pos[0] + sides[0][0], current_pos[1] + sides[0][1]), marked, graph)
            # straight, delete back to one


def floodfill(pos: tuple[int, int], marked: set[tuple[int, int]], graph: set[tuple[int, int]]):
    if (pos in marked) or (pos in graph):
        return
    if is_valid_pos(pos):
        pass
    else:
        return  # don't fill out of bounds !
    # lines[pos[1]] = lines[pos[1]][:pos[0]] + 'O' + lines[pos[1]][pos[0] + 1:]
    marked.add(pos)
    for x in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ne = (pos[0] + x[0], pos[1] + x[1])
        floodfill(ne, marked, graph)
        # if ne in graph:
            # squeeze
            # nleft = ne
            # prev = pos
            # while nleft in graph and squeeze(prev, nleft, True, graph):
            #     prev = nleft
            #     nleft = (nleft[0] + x[0], nleft[1] + x[1])
            # if nleft not in graph:
            #     floodfill(nleft, marked, graph)
            # neighbour = get_neighbour(prev, nleft, True)
            # if neighbour not in graph:
            #     floodfill(neighbour, marked, graph)
            # else:
            #     nright = ne
            #     prev = pos
            #     while nright not in graph and squeeze(prev, nright, False, graph):
            #         prev = nright
            #         nright = (nright[0] + x[0], nright[1] + x[1])
            #     if nright not in graph:
            #         floodfill(nright, marked, graph)
            #     neighbour = get_neighbour(prev, nleft, False)
            #     if neighbour not in graph:
            #         floodfill(neighbour, marked, graph)
            #
        # elif is_valid_pos(ne):


def get_graph(pos: tuple[int, int]):
    sides = get_indexes(pos)
    g = []
    previous = []
    current = []
    graph: set[tuple[int, int]] = set()
    graph.add(pos)
    # initial check, remove invalid sides
    for p in sides:
        if pos in get_indexes(p):
            g.append(1)
            previous.append(pos)
            current.append(p)
    while not np.all(current[0] == np.array(current)):
        for idx in range(len(current)):
            graph.add(current[idx])
            indexes = get_indexes(current[idx])
            indexes.remove(previous[idx])
            previous[idx] = current[idx]
            current[idx] = indexes[0]
            g[idx] += 1
    print("Q1 is", g[0])
    graph.add(current[0])
    marked: set[tuple[int, int]] = set()
    # for all points in the border, mark as outside if they aren't the loop itself
    for x in range(len(lines)):
        floodfill((x, 0), marked, graph)
        floodfill((x, len(lines[0]) - 1), marked, graph)
    for y in range(len(lines[0])):
        floodfill((0, y), marked, graph)
        floodfill((len(lines) - 1, y), marked, graph)
    mark_on_loop((5, 28), marked, graph)
    visualize(graph, marked)
    #for x in range(len(lines)):
    #    newl = lines[x]
    #    for y in range(len(lines[x])):
    #        if (y, x) not in marked and (y, x) not in graph:
    #            newl = newl[:y] + 'I' + newl[y + 1:]
    #    lines[x] = newl
    # print('\n'.join(lines))
    # visualize(graph)
    print(len(lines) * len(lines[0]) - len(marked) - len(graph))
    print("expected", 563)

def visualize(graph, marked):
    TRANSLATION = {
        ord("|"): '┃',
        ord("-"): '━',
        ord("L"): '┗',
        ord("J"): '┛',
        ord("7"): '┓',
        ord("F"): '┏',
    }
    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            c = c.translate(TRANSLATION)
            #if (c == "O" or c == 'S') and ((x, y) in graph):
            #    print(f"\033[31;5m{c}\033[0m", end="")
            if c == "S":
                print(f"\033[91m{c}\033[0m", end="")
            elif (x, y) in graph:
                print(f"\033[36m{c}\033[0m", end="")
            elif (x, y) in marked:
                print(f"\033[90m█\033[0m", end="")
            else:
                print(f"\033[32m█\033[0m", end="") # not called
        print()

for px in range(len(lines)):
    # Find S
    line = lines[px]
    if 'S' in line:
        get_graph((px, line.index('S')))
        break
