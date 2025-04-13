import random
import sys
from typing import List


class Graph(object):
    incoming: List[List[int]]
    outgoing: List[List[int]]

    vertices: int

    def __init__(self, vertices: int, density: float):
        self.vertices = vertices
        self.incoming = [[] for _ in range(vertices)]
        self.outgoing = [[] for _ in range(vertices)]

        for i in range(vertices):
            for j in range(vertices):
                vertex = random.random()
                if i != j and vertex < density:
                    self.incoming[i].append(j)
                    self.outgoing[j].append(i)


def PageRank_single(v: int, graph: Graph, ranks: List[float], damping: float):
    rank = (1 - damping) / graph.vertices
    for u in graph.incoming[v]:
        rank += damping * ranks[u] / len(graph.outgoing[u])
    return rank


def PageRank(graph: Graph, damping: float, epsilon: float = 1e-4) -> List[float]:
    ranks = [1 / graph.vertices for _ in range(graph.vertices)]
    new_ranks = [1 / graph.vertices for _ in range(graph.vertices)]

    change = epsilon + 1
    while change > epsilon:
        for v in range(graph.vertices):
            new_ranks[v] = PageRank_single(v, graph, ranks, damping)

        # Calculate difference
        change = 0
        for v in range(graph.vertices):
            change += abs(ranks[v] - new_ranks[v])

        for v in range(graph.vertices):
            ranks[v] = new_ranks[v]

    return ranks


if __name__ == "__main__":
    argv = sys.argv
    vertices = int(argv[1])
    density = float(argv[2])
    iterations = int(argv[3])

    graph = Graph(vertices, density)
    total_sum = 0

    for i in range(iterations):
        ranks = PageRank(graph, 0.85 + i / 1000.0)
        total_sum += sum(ranks)

    print(total_sum)
