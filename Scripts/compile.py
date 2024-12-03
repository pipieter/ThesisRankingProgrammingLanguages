import argparse
import os
import subprocess


ROOT = os.getcwd()


def compile(benchmark: str, language: str, verbose: bool) -> None:
    print(f"Compiling {benchmark} - {language}")

    cwd = os.path.join(ROOT, "Benchmarks", benchmark, language)
    env = os.environ

    stdin = subprocess.DEVNULL
    stdout = subprocess.DEVNULL
    stderr = subprocess.DEVNULL
    if verbose:
        stdout = subprocess.STDOUT
        stderr = subprocess.STDOUT

    process = subprocess.run(
        ["make", "compile"],
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        cwd=cwd,
        env=env,
    )

    if process.returncode != 0:
        print(process.stdout.decode("utf-8"))
        exit(1)


if __name__ == "__main__":
    benchmarks = ["PageRank"]
    languages =["C++", "Python"] # ["C#", "C++", "Java", "Python", "Rust"]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Log compilation output or not.",
    )

    args = parser.parse_args()
    verbose = args.verbose

    for benchmark in benchmarks:
        for language in languages:
            compile(benchmark, language, verbose)
