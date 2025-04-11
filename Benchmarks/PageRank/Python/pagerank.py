import sys
from typing import List


class Graph(object):
    incoming: List[List[int]]
    outgoing: List[List[int]]

    vertices: int

    def __init__(self, path: str):
        file = open(path, "r")

        line = file.readline()

        incoming_sets = []
        outgoing_sets = []
        while line != "":
            if line.startswith("p"):
                _, _, vertices, _ = line.split(" ")
                self.vertices = int(vertices)
                incoming_sets = [set() for _ in range(self.vertices)]
                outgoing_sets = [set() for _ in range(self.vertices)]

            elif line.startswith("a") or line.startswith("e"):
                elements = line.split(" ")
                a = int(elements[1])
                b = int(elements[2])

                outgoing_sets[a].add(b)
                incoming_sets[b].add(a)

            line = file.readline()

        file.close()

        # Remove duplicates
        self.outgoing = [list(s) for s in outgoing_sets]
        self.incoming = [list(s) for s in incoming_sets]


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
    file = argv[1]
    out = argv[2]

    graph = Graph(file)
    ranks = PageRank(graph, 0.85)

    with open(out, "w") as file:
        for v, rank in enumerate(ranks):
            file.write(f"{v} {rank}\n")
