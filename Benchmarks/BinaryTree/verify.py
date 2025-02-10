import argparse
import os
import os.path
import subprocess

"""
Verifies the correctness of the Binary Tree program. Python is used as a baseline to verify results.
"""


def get_output(language: str, optimized: str, size: int) -> dict[int, float]:
    cwd = os.path.abspath(f"./{language}")
    makefile = os.path.join(cwd, f"Makefile.{optimized}")

    args = os.environ
    args["ARGS"] = str(size)

    # Get command
    command = subprocess.check_output(
        ["make", "-f", makefile, "command"],
        shell=False,
        cwd=cwd,
        env=os.environ,
    ).decode("utf-8")
    command = command.strip().split(" ")

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
        help="The amount of nodes used in the comparison.",
    )

    args = parser.parse_args()
    nodes = args.nodes

    # Use Python as baseline
    print("Reading baseline")
    baseline = get_output("Python", "optimized", nodes)

    for language in ["C#", "C++", "Java", "PyPy", "Python", "Rust"]:
        for optimized in ["optimized", "unoptimized"]:
            print(f"Attempting to verify {language} ({optimized})")
            output = get_output(language, optimized, nodes)

            if output != baseline:
                print(
                    f"Verification failed for {language} ({optimized}): different output"
                )

                exit()

    print("All languages succeeded!")
