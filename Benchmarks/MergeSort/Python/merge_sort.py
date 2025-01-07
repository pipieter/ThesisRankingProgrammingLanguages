import sys
from typing import List


def split_blocks(path: str, block_size: str) -> List[List[str]]:
    blocks = []
    lines = []

    reader = open(path, "r")
    bytes_read = 0

    while True:
        line = reader.readline()
        if line == "":
            break

        lines.append(line)
        bytes_read += len(line)

        if bytes_read >= block_size:
            lines.sort(reverse=True)
            blocks.append(lines)

            lines = []
            bytes_read = 0

    if len(lines) > 0:
        lines.sort(reverse=True)
        blocks.append(lines)

    return blocks


def merge_blocks(blocks: List[List[str]]) -> List[str]:
    sorted = []

    while True:
        block = -1

        for i in range(len(blocks)):
            if len(blocks[i]) == 0:
                continue

            if block == -1:
                block = i
            else:
                current = blocks[block][-1]
                next = blocks[i][-1]

                if next < current:
                    block = i

        if block == -1:
            break

        value = blocks[block].pop()
        sorted.append(value)

    return sorted


if __name__ == "__main__":
    args = sys.argv

    file = args[1]
    out = args[2]
    block_size = int(args[3])

    blocks = split_blocks(file, block_size)
    sorted = merge_blocks(blocks)

    with open(out, "w") as file:
        file.writelines(sorted)
