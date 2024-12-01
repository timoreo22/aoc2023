f = open("day2-input.txt")
lines = f.readlines()
f.close()
color = {"red": 12, "green": 13, "blue": 14}
total = 0
for line in lines:
	num = int(line[5:line.index(':')])
	line = line[line.index(':') + 1:]
	games = line.split(';')
	impossible = False
	for game in games:
		for result in game.split(','):
			result = result[1:]
			acc = ""
			print(result)
			for c in result:
				result = result[1:]
				if c.isdigit():
					acc += c
				else:
					break
			print(acc)
			if int(acc) > color[result.strip()]:
				impossible = True
	if not impossible:
		total += num

