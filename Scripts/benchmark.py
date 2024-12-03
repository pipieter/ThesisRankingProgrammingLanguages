import json
import os
import subprocess
import time
from rich.progress import track

ROOT = os.getcwd()


def clear_caches(level: int = 3):
    os.system(f'sh -c "sync; echo {level} > /proc/sys/vm/drop_caches"')


def get_process_information(pid: int) -> dict | None:
    result = subprocess.run(["ps", "-p", str(pid), "-o", "rss"], capture_output=True)
    if result.returncode != 0:
        return None
    memory = int(result.stdout.decode("utf-8").split("\n")[1])

    result = dict()

    result["memory"] = memory

    return result


def run_benchmark(
    benchmark: str,
    benchmark_identifier: str,
    language: str,
    args: dict,
    timeout: str,
    iterations: int,
    verbose: bool = False,
    clear_cache: bool = False,
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

    # Run the program $iterations times
    energy_file_name = f"{benchmark}.{language}.{benchmark_identifier}.energy.json"
    resources_file_name = (
        f"{benchmark}.{language}.{benchmark_identifier}.resources.json"
    )

    energy_file_path = os.path.join(ROOT, "Results", energy_file_name)
    resources_file_path = os.path.join(ROOT, "Results", resources_file_name)

    args["JSON"] = energy_file_path

    description = f"{benchmark}::{benchmark_identifier}::{language}".ljust(32)
    for _ in track(range(iterations), description=description):
        try:
            if clear_cache:
                clear_caches()

            # Get (global) energy measurements
            process = subprocess.run(
                ["make", "measure"],
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
                cwd=cwd,
                timeout=timeout,
                env=args,
            )

            if verbose:
                output = process.stdout.decode("utf-8")
                if len(output) > 0:
                    print(output)

            if clear_cache:
                clear_caches()

            # Get process measurements
            process_data = dict()
            process_data["samples"] = []
            killed = False

            command = subprocess.check_output(
                ["make", "command"],
                cwd=cwd,
                env=args,
            ).decode("utf-8")

            process = subprocess.Popen(
                command,
                shell=True,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
                cwd=cwd,
                env=args,
            )

            start = time.time()
            last_measurement = start

            while process.poll() is None:
                sample = get_process_information(process.pid)

                timestamp = time.time()
                sample["runtime_ms"] = round((timestamp - last_measurement) * 1000)
                last_measurement = timestamp

                process_data["samples"].append(sample)

                if last_measurement - start > timeout:
                    process.kill()
                    killed = True

                time.sleep(0.01)
            end = time.time()

            process_data["total_runtime_ms"] = round((end - start) * 1000)
            if killed:
                process_data.samples = None

            with open(resources_file_path, "a") as file:
                json.dump(process_data, file)
                file.write("\n")

        except subprocess.TimeoutExpired:
            ...
