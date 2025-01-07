from collections import deque
from io import TextIOWrapper
import sys


class Block(object):
    file: TextIOWrapper
    block_size: int

    values: deque[str]
    file_has_remaining: bool

    def __init__(self, path: str, block_size: int):
        self.file = open(path, "r")
        self.block_size = block_size
        self.values = deque()
        self.file_has_remaining = True

    def next(self) -> str | None:
        # Read in the next block if current block is empty
        if len(self.values) == 0 and self.file_has_remaining:
            self._read_block()

        if len(self.values) > 0:
            return self.values[0]

        return None

    def pop(self) -> str:
        return self.values.popleft()

    def _read_block(self):
        if not self.file_has_remaining:
            return

        self.values.clear()

        bytes_read = 0
        while bytes_read < block_size:
            line = self.file.readline()
            if line == "":
                self.file_has_remaining = False
                return

            self.values.append(line)
            bytes_read += len(line)


def write_block(lines: list[str], index: int) -> str:
    file_name = f"block.{index}.temp"
    with open(file_name, "w") as file:
        file.writelines(lines)
    return file_name


def split_blocks(path: str, block_size: str) -> list[str]:
    files = []
    lines = []

    reader = open(path, "r")
    bytes_read = 0
    index = 0

    while True:
        line = reader.readline()
        if line == "":
            break

        lines.append(line)
        bytes_read += len(line)

        if bytes_read >= block_size:
            lines.sort()
            file_name = write_block(lines, index)

            files.append(file_name)
            lines.clear()
            bytes_read = 0
            index += 1

    if len(lines) > 0:
        lines.sort()
        file_name = write_block(lines, index)
        files.append(file_name)

    return files


def merge_blocks(files: list[str], out: str, block_size: str) -> None:
    blocks = [Block(file, block_size) for file in files]

    with open(out, "w") as writer:
        while True:
            block = -1
            value = None

            for i in range(len(blocks)):
                blockValue = blocks[i].next()
                if blockValue is None:
                    continue

                if value is None or blockValue < value:
                    block = i
                    value = blockValue

            if block == -1:
                break

            blocks[block].pop()
            writer.writelines([value])


if __name__ == "__main__":
    args = sys.argv

    file = args[1]
    out = args[2]
    block_size = int(args[3])

    files = split_blocks(file, block_size)
    merge_blocks(files, out, block_size / len(files))
