import argparse
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build(verbose: bool) -> None:
    print("Building Docker")

    stdout = subprocess.DEVNULL
    if verbose:
        stdout = None

    RAPL_path = os.path.join(ROOT, "RAPL")
    build_path = os.path.join(ROOT, "RAPL", "build")

    # Delete existing files
    subprocess.check_call(["rm", "-rf", build_path], stderr=stdout, stdout=stdout)

    subprocess.check_call(
        [
            "cmake",
            RAPL_path,
            "-B",
            build_path,
            "-DCMAKE_BUILD_TYPE=Release",
        ],
        stdout=stdout,
        stderr=stdout,
    )
    subprocess.check_call(
        ["cmake", "--build", build_path, "--parallel"],
        stdout=stdout,
        stderr=stdout,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Whether to log RAPL CMake output or not.",
    )

    args = parser.parse_args()
    verbose = args.verbose

    build(verbose=verbose)
