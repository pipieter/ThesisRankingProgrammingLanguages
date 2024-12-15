import sys
from typing import List, Set


class Graph(object):
    edges: List[Set[int]]
    vertices: int

    def __init__(self, path: str):
        file = open(path, "r")

        line = file.readline()
        while line != "":
            if line.startswith("p"):
                _, _, vertices, _ = line.split(" ")
                self.vertices = int(vertices)
                self.edges = [set() for _ in range(self.vertices)]

            elif line.startswith("a") or line.startswith("e"):
                elements = line.split(" ")
                a = int(elements[1])
                b = int(elements[2])

                if a != b:
                    self.edges[a].add(b)
                    self.edges[b].add(a)

            line = file.readline()

        file.close()


def TriangleCount_single(graph: Graph, a: int, b: int) -> int:
    if a >= b:
        return 0

    edgesA = graph.edges[a]
    edgesB = graph.edges[b]

    intersection = edgesA.intersection(edgesB)

    return len(intersection)


def TriangleCount(graph: Graph) -> int:
    count = 0

    for a in range(graph.vertices):
        for b in range(a + 1, graph.vertices):
            count += TriangleCount_single(graph, a, b)

    return count


if __name__ == "__main__":
    argv = sys.argv
    file = argv[1]

    graph = Graph(file)
    count = TriangleCount(graph)

    print(count)
