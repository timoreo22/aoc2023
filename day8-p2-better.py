from typing import Optional
import z3
from time import perf_counter
f = open("day8-input.txt")
lines = f.readlines()
f.close()
path = lines[0].strip()
lines = lines[2:]

# ASSERTIONS !!! MADE FROM GENERATED GRAPH
# There is 6 subgraph, each subgraph has exactly one A node, and exactly one Z node
# The "A" node is liked to a final node (via left child OR right child)
# The "A" node isn't used in an input
# The "Z" node is linked to a final node (via the opposite inputs to its corresponding A node)
# The length of a path from a "A" node to a "Z" node is dividable by 281 (exact looping !)

# (unused, not fully tested) Every node only has at most 2 inputs

# (untested & unused) Every single subgraph is 78 nodes long


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
# write out graph
graph = open("day8-graph.dot", "w")
print('digraph {', file=graph)
print("node [shape=record];", file=graph)
for node in nodes.values():
    extra = ""
    if node.name.endswith("A"):
        extra = ' color="green"'
    elif node.name.endswith("Z"):
        extra = ' color="red"'
    print(f'{id(node)} [label="{{<E>Entry}}|{node.name}|{{<L>Left|<R>Right}}"{extra}]', file=graph)

for node in nodes.values():
    print(f'{id(node)}:L -> {id(node.left_child)}:E', file=graph)
    print(f'{id(node)}:R -> {id(node.right_child)}:E', file=graph)


print("}", file=graph)
graph.close()
print("done")


starting_nodes: list[Node] = [] # len == 6
for node in nodes.values():
    if node.name.endswith("A"):
        starting_nodes.append(node)

s = z3.Solver()
n = z3.Int("n")  # final output !
s.add(n > 0)

cycles = {}
end_nodes = []
for node in starting_nodes:
    steps = 0
    current_node = node
    while not current_node.name.endswith("Z"):
        is_left = path[steps % len(path)]
        if is_left == 'L':
            current_node = current_node.left_child
        else:
            current_node = current_node.right_child
        # print(current_node.name)
        steps += 1
    print(node.name, "->", current_node.name, steps, steps // len(path))
    cycles[node.name] = [steps]
    end_nodes.append((node.name, current_node))
print()
print("Now with 1")
print()
for parent, node in end_nodes:
    steps = 1  # do the first step
    current_node = node.left_child
    while not current_node.name.endswith("Z"):
        is_left = path[steps % len(path)]
        if is_left == 'L':
            current_node = current_node.left_child
        else:
            current_node = current_node.right_child
        # print(current_node.name)
        steps += 1
    print(node.name, "->", current_node.name, steps, steps // len(path), steps % len(path))
    cycles[parent].append(steps)

for key, c in cycles.items():
    x = z3.Int(key)
    # s.add(n == x * (c[0] + c[1]) + b * c[0])
    s.add(n == x * c[1] + c[0])
    # s.add(x % 281 == 0) WRONG
# 12 927 600 769 609
starting = perf_counter()
if s.check() == z3.sat:
    ending = perf_counter()
    print("Time taken to solve via z3:", ending-starting)
    print(s.model())
    p = s.model()[n]
    print(p)
    # print(h.value())
    s.add(n != p)
else:
    print("No solution found")
    print(s.proof())
