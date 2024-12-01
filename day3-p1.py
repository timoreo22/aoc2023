f = open("day3-input.txt")
lines = f.readlines()
f.close()
def scan_index(xidx, yidx):
	for xoff in range(-1,2):
		for yoff in range(-1,2):
			if xidx + xoff < len(lines) and xidx + xoff > 0:
				if yidx + yoff < len(lines[xidx + xoff]) and xidx + xoff > 0:
					c = lines[xidx + xoff][yidx + yoff]
					if c != '.' and c != '\n' and not c.isdigit():
						return True
	return False

total = 0
xidx = 0
for line in lines:
	yidx = 0
	acc = ""
	valid = False
	for c in line:
		if c.isdigit():
			acc += c
			if scan_index(xidx, yidx):
				valid = True
		else:
			if valid:
				total += int(acc)
				valid = False
			acc = ""
		yidx += 1
	xidx += 1