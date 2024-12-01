f = open("day13-input.txt")
lines: list[str] = [data.strip() for data in f.readlines()]
f.close()


def getvline(line, grid):
    acc = ""
    for v in range(len(grid)):
        acc += grid[v][line]
    return acc


def check_sym(hidx, start, grid):
    while grid[hidx] == grid[start] and abs(hidx - start) >= 2:
        if hidx > start:
            hidx -= 1
            start += 1
        else:
            hidx += 1
            start -= 1
    if grid[hidx] == grid[start]:
        return max(hidx, start)
    return None


def check_vsym(vidx, start, grid):
    while getvline(vidx, grid) == getvline(start, grid) and abs(vidx - start) >= 2:
        if vidx > start:
            vidx -= 1
            start += 1
        else:
            vidx += 1
            start -= 1
    if getvline(vidx, grid) == getvline(start, grid):
        return max(vidx, start)
    return None


grid = []
total = 0
for line in lines:
    if len(line) == 0:
        # check sym Up to Down
        hidx: int | None = None
        for sym in range(1, len(grid)):
            if grid[sym] == grid[0]:
                csym = check_sym(sym, 0, grid)
                if csym is not None:
                    total += csym * 100
                    hidx = sym
                    break
        if hidx is None:
            for sym in range(len(grid) - 2, -1, -1):
                if grid[sym] == grid[len(grid) - 1]:
                    csym = check_sym(sym, len(grid) - 1, grid)
                    if csym is not None:
                        total += csym * 100
                        hidx = sym
                        break
        vidx: int | None = None
        if hidx is None:
            vline = getvline(0, grid)
            for sym in range(1, len(grid[0])):
                if vline == getvline(sym, grid):
                    csym = check_vsym(sym, 0, grid)
                    if csym is not None:
                        total += csym
                        vidx = sym
                        break

            if vidx is None:
                vline = getvline(len(grid[0]) - 1, grid)
                for sym in range(len(grid[0]) - 2, -1, -1):
                    if vline == getvline(sym, grid):
                        csym = check_vsym(sym, len(grid[0]) - 1, grid)
                        if csym is not None:
                            total += csym
                            vidx = sym
                            break
        if hidx is None and vidx is None:
            print("No symetry found ?")
        else:
            print(hidx, vidx, len(grid), len(grid[0]))
            # print(grid[0], grid[hidx], grid[len(grid) - 1])
        grid.clear()
    else:
        grid.append(line.strip())

print(total)
