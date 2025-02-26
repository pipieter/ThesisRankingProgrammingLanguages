import os
import random
import subprocess
import time
from rich.progress import track

ROOT = os.getcwd()

RAPL_PATH = os.path.abspath("./RAPL/build/rapl")


def clear_caches(level: int = 3):
    os.system(f'sh -c "sync; echo {level} > /proc/sys/vm/drop_caches"')


def get_command(cwd: str, language: str, args: dict, optimized: bool):
    makefile = f"Makefile.{language}"
    if optimized:
        command = subprocess.run(
            ["make", "-f", makefile, "command-optimized"],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=args,
        )
        if command.returncode == 0:
            return command.stdout.decode("utf-8").strip().split(" ")
        else:
            return None

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
    optimized: str,
    cwd: str,
    args: dict,
    timeout: int,
    iterations: int,
    warmups: int,
    time_between: int,
    stdin: int,
    stdout: int,
    stderr: int,
):
    # Todd Mytkowicz, Amer Diwan, Matthias Hauswirth, and Peter F. Sweeney. 2009.
    # Producing wrong data without doing anything obviously wrong!
    # SIGPLAN Not. 44, 3 (March 2009), 265–276. https://doi.org/10.1145/1508284.1508275
    args["RANDOMIZED_ENVIRONMENT_OFFSET"] = "".join(["X"] * random.randint(0, 4096))

    optimizedStr = "optimized" if optimized else "unoptimized"
    command = get_command(cwd, language, args, optimized)

    if command is None:
        return

    path = os.path.join(
        ROOT,
        "Results",
        f"{benchmark}.{optimizedStr}.{language}.{identifier}.json",
    )
    rapl_command = [RAPL_PATH, "--json", path] + command

    description = f"{benchmark}::{optimizedStr}::{identifier}::{language}".ljust(56)

    try:
        for _ in track(range(iterations), description=description):
            # Clear caches
            clear_caches()

            # Run warmups
            if warmups > 0:
                for _ in range(warmups):
                    result = subprocess.run(
                        command,
                        stdin=stdin,
                        stdout=stdout,
                        stderr=stderr,
                        cwd=cwd,
                        timeout=timeout,
                        env=args,
                    )
                    if result.returncode != 0:
                        print(f"Error running '{' '.join(command)}'")
                        print(result.stdout.decode("utf-8"))
                        print(result.stderr.decode("utf-8"))
                        exit(1)

            # Run energy measurement
            result = subprocess.run(
                rapl_command,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
                cwd=cwd,
                timeout=timeout,
                env=args,
            )
            if result.returncode != 0:
                print(f"Error running '{' '.join(rapl_command)}'")
                if result.stdout is not None:
                    print(result.stdout.decode("utf-8"))
                if result.stderr is not None:
                    print(result.stderr.decode("utf-8"))
                exit(1)
            # Sleep between iterations
            time.sleep(time_between)
    except subprocess.TimeoutExpired:
        return


def run_benchmark(
    benchmark: str,
    language: str,
    identifier: str,
    optimized: bool,
    args: dict,
    timeout: str,
    iterations: int,
    warmups: int,
    time_between: int,
    verbose: bool = False,
) -> None:
    # Copy PATH and HOME variables, this has to be done manually
    args["PATH"] = os.environ["PATH"]
    args["HOME"] = os.environ["HOME"]

    cwd = os.path.join(ROOT, "Benchmarks", benchmark)

    stdin = subprocess.DEVNULL
    stdout = subprocess.DEVNULL
    stderr = subprocess.DEVNULL
    if verbose:
        stdout = subprocess.PIPE
        stderr = subprocess.STDOUT

    run_rapl_benchmark(
        benchmark=benchmark,
        language=language,
        identifier=identifier,
        optimized=optimized,
        cwd=cwd,
        args=args,
        timeout=timeout,
        iterations=iterations,
        warmups=warmups,
        time_between=time_between,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
    )
