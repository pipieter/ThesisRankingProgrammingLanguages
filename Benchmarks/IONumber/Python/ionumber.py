import os
import sys


def read_value(path: str) -> int:
    try:
        with open(path, "r") as file:
            return int(file.read())
    except:
        return 0


def write_value(path: str, value: int) -> None:
    with open(path, "w") as file:
        file.write(str(value))


def run(count: int, path: str) -> None:
    try:
        os.remove(path)
    except:
        ...

    value = 0
    while value != count:
        value = read_value(path)
        write_value(path, value + 1)


if __name__ == "__main__":
    argv = sys.argv
    count = int(argv[1])
    path = argv[2]

    run(count, path)
