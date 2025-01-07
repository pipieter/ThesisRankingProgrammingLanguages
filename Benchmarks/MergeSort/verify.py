import argparse
import os
import os.path
import subprocess

"""
Verifies the correctness of the MergeSort algorithm. Python is used as a baseline to verify results.
"""


def get_contents(language: str, optimized: bool, path: str):
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
        return file.read()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, help="The input file to test on."
    )

    args = parser.parse_args()
    path = os.path.abspath(args.path)

    # Use Python as baseline
    print("Reading baseline")
    baseline = get_contents("Python", False, path)

    for language in ["C#", "C++", "Java", "PyPy", "Python", "Rust"]:
        for optimized in [False, True]:
            print(f"Attempting to verify {language} (optimized = {optimized})")
            contents = get_contents(language, optimized, path)
            if baseline != contents:
                print(f"Verification failed for {language} (optimized = {optimized})")
                exit()
    
    print("All languages succeeded!")
