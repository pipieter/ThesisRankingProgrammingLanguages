import sys
from typing import List
import numpy as np


class Matrix(object):
    values: np.ndarray
    n: int

    def __init__(self, n: int) -> None:
        self.n = n
        self.values = np.ndarray((n, n))


def read(path: str) -> Matrix:
    file = open(path, "r")

    n = int(file.readline())
    matrix = Matrix(n)

    index = 0
    line = file.readline()
    while line != "":
        row = index // n
        col = index % n
        matrix.values[row, col] = float(line)
        line = file.readline()
        index += 1

    file.close()

    return matrix


def write(matrix: Matrix, path: str) -> None:
    file = open(path, "w")

    file.write(f"{matrix.n}\n")

    for i in range(matrix.n):
        for j in range(matrix.n):
            file.write(f"{matrix.values[i,j]}\n")

    file.close()


def multiply(a: Matrix, b: Matrix) -> Matrix:
    assert a.n == b.n
    matrix = Matrix(a.n)
    matrix.values = np.asmatrix(a.values) * np.asmatrix(b.values)
    return matrix


if __name__ == "__main__":
    a = read(sys.argv[1])
    b = read(sys.argv[2])
    c = multiply(a, b)

    write(c, sys.argv[3])
