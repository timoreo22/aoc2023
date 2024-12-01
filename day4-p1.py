f = open("day4-input.txt")
lines = f.readlines()
f.close()
total = 0
games = {}
for line in lines:
	num = int(line[5:line.index(':')])
	line = line[line.index(':') + 1:]
	acc = ""
	winning = set()
	mine = set()
	isWinningSet = True
	for c in line:
		if c.isdigit():
			acc += c
		else:
			if c == '|':
				isWinningSet = False
			if acc == "":
				continue
			if isWinningSet:
				winning.add(int(acc))
				acc = ""
			else:
				mine.add(int(acc))
				acc = ""
	count = len(winning.intersection(mine))
	games[num] = count


def compute_game(num, win, games):
	subt = 1
	for i in range(win):
		subt += compute_game(num + i + 1, games[num + i + 1], games)
	return subt

for k,v in games.items():
	total += compute_game(k, v, games)

print(total)
