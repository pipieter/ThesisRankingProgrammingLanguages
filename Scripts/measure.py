import argparse
import os

from Scripts.benchmark import run_benchmark
from Scripts.generate_input import verify_dir


ROOT = os.getcwd()


def get_files(directory: str) -> list[str]:
    files = []
    for item in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, item)):
            files.append(item)
    return files


def measure_pagerank(languages: list[str], optimized: bool, verbose: bool) -> None:
    benchmark = "PageRank"

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
                optimized=optimized,
                args=args,
                timeout=10000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


def measure_pagerank_array(
    languages: list[str], optimized: bool, verbose: bool
) -> None:
    benchmark = "PageRankArray"

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
                optimized=optimized,
                args=args,
                timeout=10000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


def measure_external_merge_sort(languages: list[str], optimized: bool, verbose: bool) -> None:
    benchmark = "ExternalMergeSort"

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
                optimized=optimized,
                args=args,
                timeout=10000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )

def measure_merge_sort(languages: list[str], optimized: bool, verbose: bool) -> None:
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
                optimized=optimized,
                args=args,
                timeout=10000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )



def measure_setsort(languages: list[str], optimized: bool, verbose: bool) -> None:
    benchmark = "SetSort"

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
                optimized=optimized,
                args=args,
                timeout=10000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


def measure_ionumber(languages: list[str], optimized: bool, verbose: bool) -> None:
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
                optimized=optimized,
                args=args,
                timeout=10000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


def measure_fib3(languages: list[str], optimized: bool, verbose: bool) -> None:
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
                optimized=optimized,
                args=args,
                timeout=10000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


def measure_triangle_count(
    languages: list[str], optimized: bool, verbose: bool
) -> None:
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
                optimized=optimized,
                args=args,
                timeout=10000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


if __name__ == "__main__":
    LANGUAGES = ["C++", "C#", "Java", "PyPy", "Python", "Rust"]
    BENCHMARKS = [
        "PageRank",
        "ExternalMergeSort",
        "MergeSort",
        "SetSort",
        "IONumber",
        "Fib3",
        # "TriangleCount",
    ]

    BENCHMARK_MAPPINGS = {
        "PageRank": measure_pagerank,
        "ExternalMergeSort": measure_external_merge_sort,
        "MergeSort": measure_merge_sort,
        "SetSort": measure_setsort,
        "IONumber": measure_ionumber,
        "Fib3": measure_fib3,
        # "TriangleCount": measure_triangle_count,
    }

    OPTIMIZATION = ["optimized", "unoptimized"]

    parser = argparse.ArgumentParser()
    parser.add_argument("--languages", type=str, nargs="+", default=LANGUAGES)
    parser.add_argument("--benchmarks", type=str, nargs="+", default=BENCHMARKS)
    parser.add_argument("--optimized", type=str, nargs="+", default=OPTIMIZATION)
    parser.add_argument(
        "--verbose",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
    )

    args = parser.parse_args()
    languages = args.languages
    benchmarks = args.benchmarks
    optimization = args.optimized
    verbose = args.verbose

    verify_dir(os.path.join("./Results"))
    for benchmark in benchmarks:
        for opt in optimization:
            optimized = False
            if opt == "optimized":
                optimized = True
            BENCHMARK_MAPPINGS[benchmark](languages, optimized, verbose)
