import argparse
import os
import os.path
import subprocess

"""
Verifies the correctness of the Binary Tree program. Python is used as a baseline to verify results.
"""


def get_command(language: str, optimized: bool, args: dict):
    cwd = os.path.abspath(f".")
    makefile = os.path.join(cwd, f"Makefile.{language}")


    if optimized:
        result = subprocess.run(
            ["make", "-f", makefile, "command-optimized"],
            shell=False,
            cwd=cwd,
            env=args,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        # command-optimized not found, return None
        if result.returncode == 2:
            return None
        return result.stdout.decode("utf-8").strip().split(" ")

    # Get command
    command = subprocess.check_output(
        ["make", "-f", makefile, "command"],
        shell=False,
        cwd=cwd,
        env=args,
    ).decode("utf-8")
    command = command.strip().split(" ")
    return command


def get_output(language: str, optimized: bool, size: int) -> dict[int, float]:
    cwd = os.path.abspath(f".")

    args = os.environ
    args["ARGS"] = str(size)

    command = get_command(language, optimized, args)
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
        help="The amount of nodes used in the comparison.",
    )

    args = parser.parse_args()
    nodes = args.nodes

    # Use GCC as baseline
    print("Reading baseline")
    baseline = get_output("GCC", False, nodes)

    for language in ["GCC", "OpenJDK", "NET", "Mono", "CPython", "PyPy", "Rust"]:
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
