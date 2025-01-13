import argparse
import os
import os.path
import subprocess

"""
Verifies the correctness of the MergeSort algorithm. Python is used as a baseline to verify results.
"""


def get_contents(language: str, optimized: bool, path: str) -> dict[int, float]:
    out = os.path.abspath("./out.temp")
    cwd = os.path.abspath(f"./{language}")

    if os.path.isfile(out):
        os.remove(out)

    if optimized:
        makefile = cwd + "/Makefile.optimized"
    else:
        makefile = cwd + "/Makefile.unoptimized"

    args = os.environ
    args["ARGS"] = f"{path} {out} 2048"

    # Get command
    command = subprocess.check_output(
        ["make", "-f", makefile, "command"],
        shell=False,
        cwd=cwd,
        env=os.environ,
    ).decode("utf-8")
    command = command.strip().split(" ")

    # Execute command
    subprocess.run(
        command,
        shell=False,
        cwd=cwd,
        env=args,
    )

    with open(out, "r") as file:
        lines = file.readlines()
    result = dict()
    for line in lines:
        k, v = line.split(" ")
        result[int(k)] = float(v)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        type=str,
        help="The input file to test on.",
    )
    parser.add_argument(
        "--diff",
        type=float,
        help="The minimum difference between two values for them to not be equal",
        default=5e-5,
    )

    args = parser.parse_args()
    path = os.path.abspath(args.path)
    maxdiff = args.diff

    # Use Python as baseline
    print("Reading baseline")
    baseline = get_contents("Python", False, path)

    for language in ["C#", "C++", "Java", "PyPy", "Python", "Rust"]:
        for optimized in [False, True]:
            print(f"Attempting to verify {language} (optimized = {optimized})")
            contents = get_contents(language, optimized, path)

            if baseline.keys() != contents.keys():
                print(
                    f"Verification failed for {language} (optimized = {optimized}): not all keys are the same"
                )
                exit()

            for key in baseline.keys():
                diff = abs(baseline[key] - contents[key])
                if diff > maxdiff:
                    print(
                        f"Verification failed for {language} (optimized = {optimized}): key {key} has too large of a difference ({diff} > {maxdiff}) "
                    )
                    exit()

    print("All languages succeeded!")
