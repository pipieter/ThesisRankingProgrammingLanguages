import argparse
import os
import subprocess


ROOT = os.getcwd()


def compile(benchmark: str, language: str, verbose: bool) -> bool:
    print(f"Compiling {benchmark} - {language}")

    cwd = os.path.join(ROOT, "Benchmarks", benchmark, language)
    env = os.environ

    stdin = subprocess.DEVNULL
    stdout = subprocess.DEVNULL
    stderr = subprocess.DEVNULL
    if verbose:
        stdout = None
        stderr = None

    process = subprocess.run(
        ["make", "compile"],
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        cwd=cwd,
        env=env,
    )

    if process.returncode != 0:
        print(f"Could not compile {benchmark} for {language}")
        if process.stdout is not None:
            print(process.stdout.decode("utf-8"))
        if process.stderr is not None:
            print(process.stderr.decode("utf-8"))
        return False

    return True


if __name__ == "__main__":
    benchmarks = [
        "PageRank",
        "PageRankArray",
        "MergeSort",
        "SetSortOrdered",
        "SetSortUnordered",
        "IONumber",
        "Fib3",
        # "TriangleCount",
    ]
    languages = ["C#", "C++", "Java", "PyPy", "Python", "Rust"]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Log compilation output or not.",
    )
    parser.add_argument(
        "--ignore-errors",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Continue when an error occurs to the next compilation.",
    )

    args = parser.parse_args()
    verbose = args.verbose
    ignore_errors = args.ignore_errors

    for benchmark in benchmarks:
        for language in languages:
            result = compile(benchmark, language, verbose)
            if not result and not ignore_errors:
                exit(1)
