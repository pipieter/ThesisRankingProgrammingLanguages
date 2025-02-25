import sys
from typing import List

BLOCK_SIZE = 8


class Matrix(object):
    values: List[float]
    n: int

    def __init__(self, n: int) -> None:
        self.n = n
        self.values = [[0.0 for _ in range(n)] for _ in range(n)]


def read(path: str) -> Matrix:
    file = open(path, "r")

    n = int(file.readline())
    matrix = Matrix(n)

    index = 0
    while True:
        line = file.readline()
        if len(line) == 0:
            break
        row = index // n
        col = index % n
        matrix.values[row][col] = float(line)
        index += 1

    file.close()

    return matrix


def write(matrix: Matrix, path: str) -> None:
    file = open(path, "w")

    file.write(f"{matrix.n}\n")

    for i in range(matrix.n):
        for j in range(matrix.n):
            file.write(f"{matrix.values[i][j]}\n")

    file.close()


def multiply(a: Matrix, b: Matrix) -> Matrix:
    assert a.n == b.n
    matrix = Matrix(a.n)

    for kk in range(0, matrix.n, BLOCK_SIZE):
        for jj in range(0, matrix.n, BLOCK_SIZE):
            for i in range(matrix.n):
                for j in range(jj, jj + BLOCK_SIZE):
                    for k in range(kk, kk + BLOCK_SIZE):
                        matrix.values[i][j] += a.values[i][k] * b.values[k][j]

    return matrix


if __name__ == "__main__":
    a = read(sys.argv[1])
    b = read(sys.argv[2])
    c = multiply(a, b)

    write(c, sys.argv[3])
