import argparse
import os
import subprocess
import sys

import Benchmarks.MergeSort.generate as MergeSort
import Benchmarks.PageRank.generate as PageRank
from Scripts.util import verify_dir

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def generate_input_files(verbose: bool) -> None:
    # Merge sort
    verify_dir("./Data/MergeSort")
    merge_sort_lines = [4096]  # [4096, 8192, 16384, 32768]
    for lines in merge_sort_lines:
        if verbose:
            print(f"Generating MergeSort file with {lines} lines.")
        MergeSort.generate_input_file(f"./Data/MergeSort/{lines}", lines, 63)

    # Page rank
    verify_dir("./Data/PageRank")
    page_rank_vertices = [512, 1024, 2048, 4096]
    for vertices in page_rank_vertices:
        if verbose:
            print(f"Generating PageRank file with {vertices} vertices.")
        PageRank.generate_input_file(
            f"Data/PageRank/{vertices}", vertices, 0.2)


def setup(verbose: bool) -> None:
    stdout = subprocess.DEVNULL
    if verbose:
        stdout = None

    print("Generating input files...")
    generate_input_files(verbose)

    print("Building RAPL tool...")

    # subprocess.check_call(["rm", "-rf", os.path.join(ROOT, "RAPL/build")])
    subprocess.check_call(
        [
            "cmake",
            os.path.join(ROOT, "RAPL"),
            "-B",
            os.path.join(ROOT, "RAPL/build"),
            "-DCMAKE_BUILD_TYPE=Release",
        ],
        stdout=stdout,
    )
    subprocess.check_call(
        ["cmake", "--build", os.path.join(ROOT, "RAPL/build"), "--parallel"],
        stdout=stdout,
    )

    print("Building Docker")
    subprocess.check_call(
        [
            "docker",
            "build",
            "-f",
            os.path.join(ROOT, "Dockerfile"),
            "--tag",
            "thesis",
            ROOT,
        ],
        stdout=stdout,
        stderr=stdout,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", type=int, default=0)

    args = parser.parse_args()
    verbose = True if args.verbose > 0 else False

    setup(verbose)
