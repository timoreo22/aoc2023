import dataclasses

f = open("day5-input.txt")
lines = f.readlines()
f.close()


@dataclasses.dataclass(repr=True, slots=True)
class Seed:
    start: int
    end: int
    done: bool


seeds: list[Seed] = []

for line in lines:
    if line.startswith("seeds: "):
        seedtext = line[7:].split(" ")
        for s in range(0, len(seedtext), 2):
            seed = seedtext[s]
            si = int(seed.strip())
            seeds.append(Seed(si, int(seedtext[s + 1].strip()) + si, False))
    else:
        numbers = line.split(" ")
        if len(numbers) == 3:
            dest: int = int(numbers[0])
            src: int = int(numbers[1])
            rang: int = int(numbers[2])
            sidx = 0
            while sidx < len(seeds):
                if seeds[sidx].done:
                    sidx += 1
                    continue
                s = seeds[sidx]

                srce: int = src + rang
                # s.start ... src srce  ... s.end
                if s.start <= src < srce < s.end:
                    # sublist 1 [s.start;src[ (if src == s.start, empty set)
                    if s.start != src:
                        seeds.insert(sidx, Seed(s.start, src - 1, False))
                        sidx += 1
                    # sublist 2 [src;srce[ (matched set, shift by dest)
                    seeds[sidx] = Seed(dest, (srce - src) + dest - 1, True)  # shift ! - src + dest
                    # sublist 3 [srce;s.end] (if srce == s.end, empty set)
                    if srce != s.end:
                        seeds.insert(sidx + 1, Seed(srce, s.end, False))
                    sidx += 1  # probably works with 3
                # s.start .. src s.end ... srce
                elif s.start <= src <= s.end < srce:
                    # list ends in the middle
                    # sublist 1 [s.start;src[ (if src == s.start, empty set)
                    if s.start != src:
                        seeds.insert(sidx, Seed(s.start, src - 1, False))
                        sidx += 1
                    # sublist 2 [src;s.end] (shift by dest)
                    seeds[sidx] = Seed(dest, (s.end - src) + dest, True)  # shift ! - src + dest
                    sidx += 1
                # src .. s.start ... srce ... s.end
                elif src < s.start < srce < s.end:  # src > s.start is implied
                    # sublist 1 [s.start;srce[ (matched set, shift by dest)
                    seeds[sidx] = Seed((s.start - src) + dest, (srce - src) + dest - 1, True)  # shift ! - src + dest
                    # sublist 2 [srce;s.end] (if srce == s.end, empty set)
                    if srce != s.end:
                        seeds.insert(sidx + 1, Seed(srce, s.end, False))
                    sidx += 1
                # src ... s.start ... s.end ... srce
                elif src <= s.start <= s.end < srce:
                    # sublist 1 [s.start;s.end] (matched set, shift by dest)
                    seeds[sidx] = Seed((s.start - src) + dest, (s.end - src) + dest, True)  # shift ! - src + dest
                    sidx += 1
                else:
                    sidx += 1
        else:
            for s in seeds:
                s.done = False

print(min(seeds, key=lambda x: x.start).start)
