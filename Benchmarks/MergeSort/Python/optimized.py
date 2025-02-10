import multiprocessing
import sys
from typing import List

CONCURRENT_THRESHOLD = 10_000


def merge_sort_concurrent(entries: List[str]) -> None:
    if len(entries) <= 1:
        return

    half = len(entries) // 2
    left = entries[:half]
    right = entries[half:]

    merge_sort_concurrent(left)
    merge_sort_concurrent(right)

    merge(left, right, entries)


def merge_sort_parallel(entries: List[str]) -> None:
    if len(entries) <= CONCURRENT_THRESHOLD:
        merge_sort_concurrent(entries)
        return

    half = len(entries) // 2
    left = entries[:half]
    right = entries[half:]

    leftProcess = multiprocessing.Process(target=merge_sort_parallel, args=(left))
    leftProcess.start()

    merge_sort_parallel(right)

    leftProcess.join()
    leftProcess.close()

    merge(left, right, entries)


def merge(a: List[str], b: List[str], target: List[str]) -> None:
    i = 0
    ia = 0
    ib = 0

    while ia < len(a) and ib < len(b):
        if a[ia] < b[ib]:
            target[i] = a[ia]
            i += 1
            ia += 1
        else:
            target[i] = b[ib]
            i += 1
            ib += 1

    while ia < len(a):
        target[i] = a[ia]
        i += 1
        ia += 1
    while ib < len(b):
        target[i] = b[ib]
        i += 1
        ib += 1


if __name__ == "__main__":
    args = sys.argv

    input = args[1]
    output = args[2]

    with open(input, "r") as file:
        lines = file.readlines()

    merge_sort_concurrent(lines)

    with open(output, "w") as file:
        file.writelines(lines)
