import argparse
import os
import os.path
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from benchmark import get_command

"""
Verifies the correctness of the MergeSort algorithm. Python is used as a baseline to verify results.
"""


def get_contents(language: str, optimized: bool, path: str):
    out = os.path.abspath("./out.temp")
    cwd = os.path.abspath(f".")

    if os.path.isfile(out):
        os.remove(out)

    args = os.environ
    args["ARGS"] = f"{path} {out} 2048"

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
        return file.read()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="The input file to test on.")

    args = parser.parse_args()
    path = os.path.abspath(args.path)

    # Use Python as baseline
    print("Reading baseline")
    baseline = get_contents("CPython", False, path)

    for language in [
        "GCC",
        "Clang",
        "OpenJDK",
        "NET",
        "Mono",
        "CPython",
        "PyPy",
        "Rust",
    ]:
        for optimized in [False, True]:
            print(f"Attempting to verify {language} (optimized = {optimized})")
            contents = get_contents(language, optimized, path)

            if contents is None:
                # Command does not exist
                ...
            elif baseline != contents:
                print(f"Verification failed for {language} (optimized = {optimized})")
                exit()

    print("All languages succeeded!")
