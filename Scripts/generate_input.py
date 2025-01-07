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


def generate_int_list(path: str, count: int, max_value: int) -> None:
    with open(path, "w") as file:
        for _ in range(count):
            value = random.randint(0, max_value)
            file.write(f"{value}\n")


def generate_empty_file(path: str):
    with open(path, "w") as _:
        ...


def generate_merge_sort(sizes: list[int], verbose: bool) -> None:
    verify_dir("./Data/MergeSort")

    for size in sizes:
        if verbose:
            print(f"Generating MergeSort file with {size} lines.")
        generate_ids_file(f"./Data/MergeSort/{size}", size, 255)


def generate_setsort(counts: list[int], verbose: bool) -> None:
    verify_dir("./Data/SetSort")

    for count in counts:
        if verbose:
            print(f"Generating SetSort file with {count} lines.")
        generate_int_list(f"Data/SetSort/{count}", count, int(count / 20))


def generate_ionumber(counts: list[int], verbose: bool) -> None:
    verify_dir("./Data/IONumber")

    for count in counts:
        if verbose:
            print(f"Generating IONumber file with {count} lines.")
        generate_empty_file(f"Data/IONumber/{count}")


def generate_fib3(counts: list[int], verbose: bool) -> None:
    verify_dir("./Data/Fib3")

    for count in counts:
        if verbose:
            print(f"Generating Fib3 file with {count} lines.")
        generate_empty_file(f"Data/Fib3/{count}")


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

    merge_sort_inputs = [1_000, 10_000, 100_000, 1_000_000]
    setsort_inputs = [100_000, 1_000_000, 10_000_000, 100_000_000]
    ionumber_inputs = [1_000, 10_000, 100_000, 1_000_000]
    fib3_inputs = [10, 20, 30, 40]

    generate_merge_sort(merge_sort_inputs, verbose)
    generate_setsort(setsort_inputs, verbose)
    generate_ionumber(ionumber_inputs, verbose)
    generate_fib3(fib3_inputs, verbose)
