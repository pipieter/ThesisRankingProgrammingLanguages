import os

from Scripts.util.util import get_files

ROOT = os.getcwd()

OUT = os.path.abspath(os.path.join(ROOT, "out.temp"))
GRAPH_FILES = os.path.join(ROOT, "Data", "Graphs")
SORT_FILES = os.path.join(ROOT, "Data", "Sort")
MATRIX_FILES = os.path.join(ROOT, "Data", "Matrices")


def get_measure_merge_sort_args() -> list[tuple[str, str]]:
    identifiers = sorted(get_files(SORT_FILES), key=int)

    args = []
    for identifier in identifiers:
        path = os.path.join(SORT_FILES, identifier)
        arg = f"{path} {OUT}"
        args.append((identifier, arg))

    return args


def get_measure_pagerank_args() -> list[tuple[str, str]]:
    identifiers = sorted(get_files(GRAPH_FILES), key=int)

    args = []
    for identifier in identifiers:
        path = os.path.join(GRAPH_FILES, identifier)
        arg = f"{path} {OUT}"
        args.append((identifier, arg))

    return args


def get_measure_io_number_args() -> list[tuple[str, str]]:
    args = []

    for num in [2**14, 2**15, 2**16, 2**17]:
        args.append((str(num), f"{num} {OUT}"))

    return args


def get_measure_binarytree_args() -> list[tuple[str, str]]:
    args = []
    for num in [2**24, 2**25, 2**26, 2**27]:
        args.append((str(num), str(num)))

    return args

def get_measure_matmul_args() ->  list[tuple[str, str]]:
    identifiers = sorted(get_files(MATRIX_FILES), key=int)

    args = []
    for identifier in identifiers:
        path = os.path.join(MATRIX_FILES, identifier)
        arg = f"{path} {path} {OUT}"
        args.append((identifier, arg))

    return args