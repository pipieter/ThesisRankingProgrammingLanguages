import sys

# Note: this is the same implementation the unordered set, as Python does not have an ordered set data structure


def set_sort(in_file: str, out_file: str) -> None:
    values = set()

    # Read file
    with open(in_file, "r") as file:
        for line in file:
            values.add(int(line))

    # Write file
    with open(out_file, "w") as file:
        for value in sorted(values):
            file.write(f"{value}\n")


if __name__ == "__main__":
    argv = sys.argv
    in_file = argv[1]
    out_file = argv[2]

    set_sort(in_file, out_file)
