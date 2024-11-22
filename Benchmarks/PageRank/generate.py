import argparse
import random


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num")
    parser.add_argument("--density", default=0.2)

    args = parser.parse_args()
    vertices = int(args.num)
    density = float(args.density)

    edges = set()

    while len(edges) < density * vertices * (vertices - 1):
        a = random.randint(0, vertices - 1)
        b = random.randint(0, vertices - 1)
        edges.add((a, b))

    with open(f"out.{vertices}.graph", "w") as file:
        file.write(f"{vertices}\n")
        for edge in edges:
            file.write(f"{edge[0]} {edge[1]}\n")
