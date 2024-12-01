from typing import Optional
import tqdm

f = open("day8-input.txt")
lines = f.readlines()
f.close()
path = lines[0].strip()
lines = lines[2:]


class Node:
    left_child: Optional["Node"] = None
    right_child: Optional["Node"] = None

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"{self.name} = ({self.left_child.name}, {self.right_child.name})"


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
total_steps = 0
starting_nodes: list[Node] = [] # len == 6
for node in nodes.values():
    if node.name.endswith("A"):
        starting_nodes.append(node)

with tqdm.tqdm() as pbar:
    while True:
        pbar.update()
        ending = True
        for nc in range(len(starting_nodes)):
            current_node = starting_nodes[nc]
            is_left = path[total_steps % len(path)]
            if is_left == 'L':
                starting_nodes[nc] = current_node.left_child
            else:
                starting_nodes[nc] = current_node.right_child
            if not starting_nodes[nc].name.endswith("Z"):
                ending = False

        total_steps += 1
        if ending:
            break
print(total_steps)
