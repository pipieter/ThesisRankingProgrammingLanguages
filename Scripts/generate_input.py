import argparse
import os

import Benchmarks.MergeSort.generate as MergeSort
import Benchmarks.PageRank.generate as PageRank


def verify_dir(dir: str) -> None:
    if not os.path.exists(dir):
        os.makedirs(dir)


def generate_merge_sort(sizes: list[int], verbose: bool) -> None:
    verify_dir("./Data/MergeSort")

    for size in sizes:
        if verbose:
            print(f"Generating MergeSort file with {size} lines.")
        MergeSort.generate_input_file(f"./Data/MergeSort/{size}", size, 63)


def generate_pagerank(vertex_counts: list[int], verbose: bool) -> None:
    verify_dir("./Data/PageRank")

    for vertex_count in vertex_counts:
        if verbose:
            print(f"Generating PageRank file with {vertex_count} vertices.")
        PageRank.generate_input_file(f"Data/PageRank/{vertex_count}", vertex_count, 0.2)


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

    generate_merge_sort([512, 1024, 2048, 4096], verbose)
    generate_pagerank([512, 1024, 2048, 4096], verbose)
