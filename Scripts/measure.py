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


def measure_setsort(languages: list[str], verbose: bool) -> None:
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
                args=args,
                timeout=1000,
                iterations=1,
                verbose=verbose,
                clear_cache=True,
            )


if __name__ == "__main__":
    languages = ["C++", "C#", "Java", "PyPy", "Python", "Rust"]
    verbose = True

    # measure_pagerank(languages, verbose)
    # measure_merge_sort(languages, verbose)
    measure_setsort(languages, verbose)
