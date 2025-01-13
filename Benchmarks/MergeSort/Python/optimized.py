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
    merged = [None] * (len(a) + len(b))
    i = 0
    ia = 0
    ib = 0

    while ia < len(a) and ib < len(b):
        if a[ia] < b[ib]:
            merged[i] = a[ia]
            i += 1
            ia += 1
        else:
            merged[i] = b[ib]
            i += 1
            ib += 1
      
    while ia < len(a):
        merged[i] = a[ia]
        i += 1
        ia += 1
    while ib < len(b):
        merged[i] = b[ib]
        i += 1
        ib += 1

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
