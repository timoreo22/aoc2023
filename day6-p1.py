import z3
f = open("day6-input.txt")
lines = f.readlines()
f.close()

times = [int(x.strip()) for x in lines[0].split(" ") if x.strip().isdigit()]
distance = [int(x.strip()) for x in lines[1].split(" ") if x.strip().isdigit()]
# durée pour n : (x - n) * n
x = times[0]

n = z3.Int("n")
s = z3.Solver()
s.add((x - n) * n > distance[0])
res = s.check()
while res == z3.sat:
    m = s.model()
    print(m)
    block = []
    for var in m:
        block.append(var() != m[var])
    s.add(z3.Or(block))
    res = s.check()

print(times, distance)
