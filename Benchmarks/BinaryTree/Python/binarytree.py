from math import ceil, floor, log2
import sys


class Node(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right


def build(nodes):
    if nodes == 0:
        return None

    nodesLeft = int(floor(nodes / 2))
    nodesRight = nodes - nodesLeft - 1

    left = build(nodesLeft)
    right = build(nodesRight)
    return Node(left, right)


def count(tree, depth, target):
    if tree is None:
        return

    target[depth] += 1
    count(tree.left, depth + 1, target)
    count(tree.right, depth + 1, target)


if __name__ == "__main__":
    nodes = int(sys.argv[1])
    depth = int(ceil(log2(nodes))) + 1
    tree = build(nodes)
    counts = [0 for _ in range(depth)]

    count(tree, 0, counts)

    for i in range(depth):
        print(f"{i} {counts[i]}")
