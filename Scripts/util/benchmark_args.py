import os

from Scripts.util.util import get_files

ROOT = os.getcwd()


GRAPH_FILES = os.path.join(ROOT, "Data", "Graphs")
SORT_FILES = os.path.join(ROOT, "Data", "Sort")


def get_measure_merge_sort_args() -> list[tuple[str, str]]:
    identifiers = sorted(get_files(SORT_FILES), key=int)

    args = []
    for identifier in identifiers:
        path = os.path.join(SORT_FILES, identifier)
        arg = f"{path} out.temp"
        args.append((identifier, arg))

    return args


def get_measure_external_merge_sort_args() -> list[tuple[str, str]]:
    identifiers = sorted(get_files(SORT_FILES), key=int)

    args = []
    for identifier in identifiers:
        path = os.path.join(SORT_FILES, identifier)
        arg = f"{path} out.temp 8192"
        args.append((identifier, arg))

    return args


def get_measure_pagerank_args() -> list[tuple[str, str]]:
    identifiers = sorted(get_files(GRAPH_FILES), key=int)

    args = []
    for identifier in identifiers:
        path = os.path.join(GRAPH_FILES, identifier)
        arg = f"{path} out.temp"
        args.append((identifier, arg))

    return args


def get_measure_io_number_args() -> list[tuple[str, str]]:
    args = []

    for num in [1_000, 10_000, 100_000, 1_000_000]:
        args.append((str(num), f"{num} out.temp"))

    return args


def get_measure_io_number_args() -> list[tuple[str, str]]:
    args = []

    for num in [1_000, 10_000, 100_000, 1_000_000]:
        args.append((str(num), f"{num} out.temp"))

    return args


def get_measure_fib3_args() -> list[tuple[str, str]]:
    args = []
    for num in [10, 20, 30, 40]:
        args.append((str(num), str(num)))

    return args
