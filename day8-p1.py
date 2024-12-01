from typing import Optional

f = open("day8-input.txt")
lines = f.readlines()
f.close()
path = lines[0].strip()
lines = lines[2:]


class Node:
    left_child: Optional["Node"] = None
    right_child: Optional["Node"] = None

    def __init__(self, name):
        self.name = name


nodes: dict[str, Node] = {}
for line in lines:
    n: str
    childs: str
    n, childs = line.split('=')
    n = n.strip()
    left, right = childs.split(',')
    left = left.strip()[1:]
    right = right.strip()
    right = right[:len(right)-1]
    node = nodes.setdefault(n, Node(n))
    node.left_child = nodes.setdefault(left, Node(left))
    node.right_child = nodes.setdefault(right, Node(right))

# Go from AAA
steps = 0
current_node = nodes["AAA"]
while current_node.name != "ZZZ":
    is_left = path[steps % len(path)]
    if is_left == 'L':
        current_node = current_node.left_child
    else:
        current_node = current_node.right_child
    print(current_node.name)
    steps += 1
print(len(path))
print(steps % len(path))
print(steps // len(path))
print(steps)
