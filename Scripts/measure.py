import argparse
import os

from Scripts.benchmark import run_benchmark


ROOT = os.getcwd()


def get_files(directory: str) -> list[str]:
    files = []
    for item in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, item)):
            files.append(item)
    return files


def measure_pagerank(languages: list[str], verbose: bool) -> None:
    benchmark = "PageRank"

    input_dir = os.path.join(ROOT, "Data", "PageRank")
    files = [int(file) for file in get_files(input_dir)]
    files = sorted(files)

    for file in files:
        filepath = os.path.join(input_dir, str(file))
        out = os.path.join(ROOT, "out.temp")

        args = dict()
        args["ARGS"] = f'"{filepath}" "{out}"'

        for language in languages:
            run_benchmark(
                benchmark=benchmark,
                benchmark_identifier=str(file),
                language=language,
                args=args,
                timeout=1000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


def measure_merge_sort(languages: list[str], verbose: bool) -> None:
    benchmark = "MergeSort"

    input_dir = os.path.join(ROOT, "Data", "MergeSort")
    files = [int(file) for file in get_files(input_dir)]
    files = sorted(files)

    for file in files:
        filepath = os.path.join(input_dir, str(file))
        out = os.path.join(ROOT, "out.temp")

        args = dict()
        args["ARGS"] = f'"{filepath}" "{out}" 512000'

        for language in languages:
            run_benchmark(
                benchmark=benchmark,
                benchmark_identifier=str(file),
                language=language,
                args=args,
                timeout=1000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


def measure_setsort_ordered(languages: list[str], verbose: bool) -> None:
    benchmark = "SetSortOrdered"

    input_dir = os.path.join(ROOT, "Data", "SetSort")
    files = [int(file) for file in get_files(input_dir)]
    files = sorted(files)

    for file in files:
        filepath = os.path.join(input_dir, str(file))
        out = os.path.join(ROOT, "out.temp")

        args = dict()
        args["ARGS"] = f'"{filepath}" "{out}" 512000'

        for language in languages:
            run_benchmark(
                benchmark=benchmark,
                benchmark_identifier=str(file),
                language=language,
                args=args,
                timeout=1000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


def measure_setsort_unordered(languages: list[str], verbose: bool) -> None:
    benchmark = "SetSortUnordered"

    input_dir = os.path.join(ROOT, "Data", "SetSort")
    files = [int(file) for file in get_files(input_dir)]
    files = sorted(files)

    for file in files:
        filepath = os.path.join(input_dir, str(file))
        out = os.path.join(ROOT, "out.temp")

        args = dict()
        args["ARGS"] = f'"{filepath}" "{out}" 512000'

        for language in languages:
            run_benchmark(
                benchmark=benchmark,
                benchmark_identifier=str(file),
                language=language,
                args=args,
                timeout=1000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


def measure_ionumber(languages: list[str], verbose: bool) -> None:
    benchmark = "IONumber"

    input_dir = os.path.join(ROOT, "Data", "IONumber")
    files = [int(file) for file in get_files(input_dir)]
    files = sorted(files)

    for file in files:
        out = os.path.join(ROOT, "out.temp")

        args = dict()
        args["ARGS"] = f'{file} "{out}" 512000'

        for language in languages:
            run_benchmark(
                benchmark=benchmark,
                benchmark_identifier=str(file),
                language=language,
                args=args,
                timeout=1000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


def measure_fib3(languages: list[str], verbose: bool) -> None:
    benchmark = "Fib3"

    input_dir = os.path.join(ROOT, "Data", "Fib3")
    files = [int(file) for file in get_files(input_dir)]
    files = sorted(files)

    for file in files:
        out = os.path.join(ROOT, "out.temp")

        args = dict()
        args["ARGS"] = f"{file}"

        for language in languages:
            run_benchmark(
                benchmark=benchmark,
                benchmark_identifier=str(file),
                language=language,
                args=args,
                timeout=1000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


def measure_triangle_count(languages: list[str], verbose: bool) -> None:
    benchmark = "TriangleCount"

    input_dir = os.path.join(ROOT, "Data", "Graphs")
    files = [int(file) for file in get_files(input_dir)]
    files = sorted(files)

    for file in files:
        filepath = os.path.join(input_dir, str(file))
        out = os.path.join(ROOT, "out.temp")

        args = dict()
        args["ARGS"] = f'"{filepath}" "{out}"'

        for language in languages:
            run_benchmark(
                benchmark=benchmark,
                benchmark_identifier=str(file),
                language=language,
                args=args,
                timeout=1000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


if __name__ == "__main__":
    LANGUAGES = ["C++", "C#", "Java", "PyPy", "Python", "Rust"]
    BENCHMARKS = [
        "PageRank",
        "MergeSort",
        "SetSortOrdered",
        "SetSortOrdered",
        "IONumber",
        "Fib3",
        "TriangleCount",
    ]

    BENCHMARK_MAPPINGS = {
        "PageRank": measure_pagerank,
        "MergeSort": measure_merge_sort,
        "SetSortOrdered": measure_setsort_ordered,
        "SetSortUnordered": measure_setsort_unordered,
        "IONumber": measure_ionumber,
        "Fib3": measure_fib3,
        "TriangleCount": measure_triangle_count,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("--languages", type=str, nargs="+", default=LANGUAGES)
    parser.add_argument("--benchmarks", type=str, nargs="+", default=BENCHMARKS)
    parser.add_argument(
        "--verbose",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
    )

    args = parser.parse_args()
    languages = args.languages
    benchmarks = args.benchmarks
    verbose = args.verbose

    for benchmark in benchmarks:
        BENCHMARK_MAPPINGS[benchmark](languages, verbose)
