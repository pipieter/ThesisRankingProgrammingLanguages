import sys
from typing import List


def merge_sort(entries: List[str]) -> List[str]:
    if len(entries) <= 1:
        return entries

    half = len(entries) // 2
    left = merge_sort(entries[:half])
    right = merge_sort(entries[half:])

    return merge(left, right)


def merge(a: List[str], b: List[str]) -> List[str]:
    merged = []
    ia = 0
    ib = 0

    while ia < len(a) and ib < len(b):
        if a[ia] < b[ib]:
            merged.append(a[ia])
            ia += 1
        else:
            merged.append(b[ib])
            ib += 1

    merged.extend(a[ia:])
    merged.extend(b[ib:])

    return merged


if __name__ == "__main__":
    args = sys.argv

    input = args[1]
    output = args[2]

    with open(input, "r") as file:
        lines = file.readlines()

    sorted = merge_sort(lines)

    with open(output, "w") as file:
        file.writelines(sorted)
