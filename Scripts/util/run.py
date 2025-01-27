import json
import os
import random
import subprocess
import time
from rich.progress import track

ROOT = os.getcwd()

RAPL_PATH = os.path.abspath("../RAPL/build/rapl")


def clear_caches(level: int = 3):
    os.system(f'sh -c "sync; echo {level} > /proc/sys/vm/drop_caches"')


def get_command(cwd: str, makefile: str, args: dict):
    command = subprocess.check_output(
        ["make", "-f", makefile, "command"],
        cwd=cwd,
        env=args,
    ).decode("utf-8")
    command = command.strip().split(" ")
    return command


def run_rapl_benchmark(
    benchmark: str,
    language: str,
    identifier: str,
    optimizedStr: str,
    makefile: str,
    cwd: str,
    args: dict,
    timeout: int,
    iterations: int,
    warmups: int,
    stdin: int,
    stdout: int,
    stderr: int,
):
    # Todd Mytkowicz, Amer Diwan, Matthias Hauswirth, and Peter F. Sweeney. 2009.
    # Producing wrong data without doing anything obviously wrong!
    # SIGPLAN Not. 44, 3 (March 2009), 265–276. https://doi.org/10.1145/1508284.1508275
    args["RANDOMIZED_ENVIRONMENT_OFFSET"] = "".join(["X"] * random.randint(0, 4096))

    command = get_command(cwd, makefile, args)

    path = os.path.join(
        ROOT,
        "Results",
        f"{benchmark}.{optimizedStr}.{language}.{identifier}.json",
    )
    rapl_command = [RAPL_PATH, "--json", path] + command

    description = f"{benchmark}::{optimizedStr}::{identifier}::{language}".ljust(56)

    for _ in track(range(iterations), description=description):
        # Clear caches
        clear_caches()

        # Run warmups
        if warmups > 0:
            for _ in range(warmups):
                subprocess.run(
                    command,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=stderr,
                    cwd=cwd,
                    timeout=timeout,
                    env=args,
                )

        # Run energy measurement
        subprocess.run(
            rapl_command,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            cwd=cwd,
            timeout=timeout,
            env=args,
        )

        # Sleep between iterations
        time.sleep(5)


def run_benchmark(
    benchmark: str,
    language: str,
    identifier: str,
    optimized: bool,
    args: dict,
    timeout: str,
    iterations: int,
    warmups: int,
    verbose: bool = False,
) -> None:
    # Copy PATH and HOME variables, this has to be done manually
    args["PATH"] = os.environ["PATH"]
    args["HOME"] = os.environ["HOME"]

    cwd = os.path.join(ROOT, "Benchmarks", benchmark, language)

    stdin = subprocess.DEVNULL
    stdout = subprocess.DEVNULL
    stderr = subprocess.DEVNULL
    if verbose:
        stdout = subprocess.PIPE
        stderr = subprocess.STDOUT

    if optimized:
        optimizedStr = "optimized"
        makefile = "Makefile.optimized"
    else:
        optimizedStr = "unoptimized"
        makefile = "Makefile.unoptimized"

    run_rapl_benchmark(
        benchmark=benchmark,
        language=language,
        identifier=identifier,
        optimizedStr=optimizedStr,
        makefile=makefile,
        cwd=cwd,
        args=args,
        timeout=timeout,
        iterations=iterations,
        warmups=warmups,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
    )
