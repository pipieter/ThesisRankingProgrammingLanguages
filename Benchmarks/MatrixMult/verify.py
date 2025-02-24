import argparse
import os
import os.path
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from benchmark import get_command

"""
Verifies the correctness of the MatrixMult algorithm. GCC is used as a baseline to verify results.
"""


def get_contents(language: str, optimized: bool, path: str):
    out = os.path.abspath("./out.temp")
    cwd = os.path.abspath(f".")

    if os.path.isfile(out):
        os.remove(out)

    args = os.environ
    args["ARGS"] = f"{path} {path} {out}"

    command = get_command(language, optimized, cwd, args)
    if command is None:
        return None

    # Execute command
    subprocess.run(
        command,
        shell=False,
        cwd=cwd,
        env=args,
    )

    with open(out, "r") as file:
        data = []
        for line in file.readlines():
            data.append(float(line))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="The input file to test on.")
    parser.add_argument(
        "--threshold", type=float, default=1e-4, help="The input file to test on."
    )

    args = parser.parse_args()
    path = os.path.abspath(args.path)
    threshold = float(args.threshold)

    # Use Python as baseline
    print("Reading baseline")
    baseline = get_contents("GCC", False, path)

    for language in [
        "GCC",
        "Clang",
        "OpenJDK",
        "NET",
        "Mono",
        # "CPython",  # CPython not included because of performance
        "PyPy",
        "Rust",
    ]:
        for optimized in [False, True]:
            print(f"Attempting to verify {language} (optimized = {optimized})")
            contents = get_contents(language, optimized, path)

            if contents is None:
                # Command does not exist
                continue

            for i in range(len(baseline)):
                if abs(baseline[i] - contents[i]) > threshold:
                    print(
                        f"Difference between baseline and {language} (optimized = {optimized})"
                    )

    print("All languages succeeded!")
