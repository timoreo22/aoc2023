valid = ["one","two","three","four","five","six","seven","eight","nine"]
total = 0
for l in lines:
	first = None
	second = None
	for substr in range(len(l)):
		c = l[substr]
		for i in range(len(valid)):
			if l[substr:].startswith(valid[i]):
				if first is None:
					first = i + 1
				else:
					second = i + 1
		if c.isdigit():
			if first is None:
				first = int(c)
			else:
				second = int(c)
	if second is None:
		total += int(str(first) + str(first))
	else:
		total += int(str(first) + str(second))