import argparse
import os
import os.path
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from benchmark import get_command


"""
Verifies the correctness of the Binary Tree program. Python is used as a baseline to verify results.
"""


def get_output(language: str, optimized: bool, size: int) -> dict[int, float]:
    cwd = os.path.abspath(f".")

    args = os.environ
    args["ARGS"] = str(size)

    command = get_command(language, optimized, cwd, args)
    if command is None:
        return None
    # Execute command
    out = subprocess.check_output(
        command,
        shell=False,
        cwd=cwd,
        env=args,
    ).decode("utf-8")

    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "nodes",
        type=int,
        help="The number of nodes used in the comparison.",
    )

    args = parser.parse_args()
    nodes = args.nodes

    # Use GCC as baseline
    print("Reading baseline")
    baseline = get_output("GCC", False, nodes)

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
            output = get_output(language, optimized, nodes)
            if output is None:
                # print(f"Skipping {language} (optimized = {optimized})")
                ...
            elif output != baseline:
                print(
                    f"Verification failed for {language} ({optimized}): different output"
                )

                print()
                print("Baseline")
                print(baseline)

                print("Output")
                print(output)

                exit()

    print("All languages succeeded!")
