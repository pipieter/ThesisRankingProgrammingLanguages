import argparse
import os
import subprocess


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build(verbose: bool) -> None:
    print("Building Docker")

    stdout = subprocess.DEVNULL
    if verbose:
        stdout = None

    process = subprocess.run(
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

    if process.returncode != 0:
        if process.stdout is not None:
            print(process.stdout.decode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Whether to log Docker output or not.",
    )

    args = parser.parse_args()
    verbose = args.verbose

    build(verbose=verbose)
