import sys
import numpy as np


def read(path: str) -> np.ndarray:
    file = open(path, "r")
    lines = file.readlines()
    file.close()

    n = int(lines[0])
    values = [float(value) for value in lines[1:]]
    values = np.asarray(values, dtype=np.float32)
    values = np.reshape(values, (n, n))

    return values


def write(matrix: np.ndarray, path: str) -> None:
    file = open(path, "w")

    file.write(f"{matrix.shape[0]}\n")
    matrix = np.reshape(matrix, matrix.shape[0] * matrix.shape[1])
    values = map(str, matrix)
    file.write("\n".join(values))
    file.write("\n")

    file.close()


def multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b


if __name__ == "__main__":
    a = read(sys.argv[1])
    b = read(sys.argv[2])
    c = multiply(a, b)

    write(c, sys.argv[3])
