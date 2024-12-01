from collections import Counter
from functools import cmp_to_key, lru_cache

f = open("day7-input.txt")
lines = f.readlines()
f.close()
hands = []
for line in lines:
    handp, number = line.split()
    hands.append((handp, int(number)))

order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


def tiebreaker(hand1, hand2) -> int:
    for c in range(len(hand1)):
        i = order.index(hand2[c]) - order.index(hand1[c])
        if i != 0:
            return i
    return 0


@lru_cache(maxsize=None)
def get_score(hand) -> int:
    c = Counter(hand)
    val = list(c.values())
    if 5 in val:
        return 6
    if 4 in val:
        return 5
    if 3 in val and 2 in val:
        return 4
    if 3 in val:
        return 3
    if val.count(2) == 2:
        return 2
    if 2 in val:
        return 1
    return 0


def cmp_hands(hand1, hand2) -> int:
    diff = get_score(hand1[0]) - get_score(hand2[0])
    if diff == 0:
        return tiebreaker(hand1[0], hand2[0])
    return diff


hands.sort(key=cmp_to_key(cmp_hands))
print(hands)
total = 0
for h in range(len(hands)):
    handbid = hands[h][1]
    total += handbid * (h + 1)
print(total)
