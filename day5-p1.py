f = open("day5-input.txt")
lines = f.readlines()
f.close()
seeds = []
done = []
for line in lines:
    if line.startswith("seeds: "):
        for seed in line[7:].split(" "):
            seeds.append(int(seed.strip()))
            done.append(False)
        print(seeds)
    else:
        numbers = line.split(" ")
        if len(numbers) == 3:
            dest = int(numbers[0])
            src = int(numbers[1])
            rang = int(numbers[2])
            print(dest, src, rang)
            for sidx in range(len(seeds)):
                if done[sidx]:
                    continue
                s = seeds[sidx]
                if src <= s < (src + rang):
                    print(s, "is valid, makes", s, "-", src, "+", dest, "=", (s - src) + dest)
                    seeds[sidx] = (s - src) + dest
                    done[sidx] = True
        else:
            print(line, end="")
            for i in range(len(done)):
                done[i] = False

print(min(seeds))
