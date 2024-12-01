import functools
from collections import Counter
from functools import cmp_to_key

f = open("day7-input.txt")
lines = f.readlines()
f.close()
hands = []
for line in lines:
    handp, number = line.split()
    hands.append((handp, int(number)))

order = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def tiebreaker(hand1, hand2) -> int:
    for c in range(len(hand1)):
        i = order.index(hand2[c]) - order.index(hand1[c])
        if i != 0:
            return i
    return 0


@functools.lru_cache(maxsize=None)
def get_score(hand) -> int:
    c = Counter(hand)
    jokers = c["J"]
    del c["J"]
    val = list(c.values())
    if jokers >= 4:
        return 6  # 5 same
    if 5 - jokers in val:
        return 6  # 5 same

    if 4 - jokers in val:
        return 5  # 4 same

    if 3 in val and 2 in val:
        return 4  # full house
    if val.count(2) == 2 and jokers == 1:
        return 4  # full house

    if 3 - jokers in val:
        return 3  # triple
    if val.count(2) == 2:
        return 2  # double paire
    if 2 - jokers in val:
        return 1  # paire
    return 0  # rien


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
print(get_score.cache_info())
print(total)
