f = open("day2-input.txt")
lines = f.readlines()
f.close()
total = 0
for line in lines:
	num = int(line[5:line.index(':')])
	line = line[line.index(':') + 1:]
	games = line.split(';')
	power = 1
	maxs = {"red": 0, "green": 0, "blue": 0}
	for game in games:
		for result in game.split(','):
			result = result[1:]
			acc = ""
			for c in result:
				result = result[1:]
				if c.isdigit():
					acc += c
				else:
					break
			maxs[result.strip()] = max(maxs[result.strip()], int(acc))
	for v in maxs.values():
		print(v)
		power *= v
	total += power

