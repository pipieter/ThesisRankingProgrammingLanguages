import sys


class Graph(object):
    incoming: list[set[int]]
    outgoing: list[set[int]]

    vertices: int

    def __init__(self, path: str):
        file = open(path, "r")

        line = file.readline()
        while line != "":
            if line.startswith("p"):
                _, _, vertices, _ = line.split(" ")
                self.vertices = int(vertices)
                self.incoming = [set() for _ in range(self.vertices)]
                self.outgoing = [set() for _ in range(self.vertices)]

            elif line.startswith("a") or line.startswith("e"):
                elements = line.split(" ")
                a = int(elements[1])
                b = int(elements[2])

                self.outgoing[a].add(b)
                self.incoming[b].add(a)

            line = file.readline()

        file.close()


def PageRank_single(v: int, graph: Graph, ranks: list[float], damping: float):
    rank = (1 - damping) / graph.vertices
    for u in graph.incoming[v]:
        rank += damping * ranks[u] / len(graph.outgoing[u])
    return rank


def PageRank(graph: Graph, damping: float, epsilon: float = 1e-4) -> list[float]:
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
