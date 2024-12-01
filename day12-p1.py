f = open("day12-input.txt")
lines: list[str] = [data.strip() for data in f.readlines() if len(data.strip()) > 0]
f.close()

for line in lines:
    puzzle, r = line.split()
    blocks: list[int] = [int(x) for x in r.split(',')]
    blocks.reverse()
    pos = 0
    for b in blocks:
        # blocks is reversed !!
        for l in range(b):
            pass
