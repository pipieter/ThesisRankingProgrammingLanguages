import argparse
import os
import random
import string


def verify_dir(dir: str) -> None:
    if not os.path.exists(dir):
        os.makedirs(dir)


def generate_id(length: int) -> str:
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
    chars = random.choices(alphabet, k=length)
    return "".join(chars)


def generate_ids_file(path: str, lines: int, id_length: int) -> None:
    file = open(path, "w")

    for _ in range(lines):
        id = generate_id(id_length)
        file.write(id + "\n")

    file.close()


def generate_sort(sizes: list[int], verbose: bool) -> None:
    verify_dir("./Data/Sort")

    for size in sizes:
        if verbose:
            print(f"Generating Sort file with {size} lines.")
        generate_ids_file(f"./Data/Sort/{size}", size, 255)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Print extra information.",
    )

    args = parser.parse_args()
    verbose = args.verbose

    sort_inputs = [1_000, 10_000, 100_000, 1_000_000]

    # Graphs are currently created elsewhere
    generate_sort(sort_inputs, verbose)
