from collections import deque
from io import TextIOWrapper
import sys


def fib3(value: int) -> int:
    if value == 0:
        return 0
    if value == 1:
        return 1
    if value == 2:
        return 1

    return fib3(value - 1) + fib3(value - 2) + fib3(value - 3)


if __name__ == "__main__":
    args = sys.argv

    value = int(args[1])
    result = fib3(value)

    print(result)
