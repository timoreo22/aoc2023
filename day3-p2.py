f = open("day3-input.txt")
lines = f.readlines()
f.close()
def scan_index(xidx, yidx):
	for xoff in range(-1,2):
		for yoff in range(-1,2):
			if xidx + xoff < len(lines) and xidx + xoff > 0:
				if yidx + yoff < len(lines[xidx + xoff]) and xidx + xoff > 0:
					c = lines[xidx + xoff][yidx + yoff]
					if c == '*':
						return xidx + xoff, yidx + yoff
	return None

gears = {}
total = 0
xidx = 0
for line in lines:
	yidx = 0
	acc = ""
	gear = None
	for c in line:
		if c.isdigit():
			acc += c
			if gear is None:
				gear = scan_index(xidx, yidx)
		else:
			if gear is not None:
				gears.setdefault(gear, []).append(int(acc))
				gear = None
			acc = ""
		yidx += 1
	xidx += 1

for v in gears.values():
	if len(v) == 2:
		total += v[0] * v[1]

print(total)