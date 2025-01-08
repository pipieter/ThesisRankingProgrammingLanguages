import json
import os
import subprocess
import time
from rich.progress import track

ROOT = os.getcwd()

RAPL_PATH = os.path.abspath("./RAPL/build/rapl")


def clear_caches(level: int = 3):
    os.system(f'sh -c "sync; echo {level} > /proc/sys/vm/drop_caches"')


def get_process_memory(pid: int) -> tuple[bool, int, int]:
    result = subprocess.run(["cat", f"/proc/{pid}/smaps_rollup"], capture_output=True)
    if result.returncode != 0:
        return False, 0, 0

    lines = result.stdout.decode("utf-8").split("\n")
    shared_memory = 0
    private_memory = 0

    for line in lines:
        if line.startswith("Shared"):
            memory = list(filter(None, line.split(" ")))
            memory = int(memory[1])
            shared_memory += memory
        elif line.startswith("Private"):
            memory = list(filter(None, line.split(" ")))
            memory = int(memory[1])
            private_memory += memory

    return True, shared_memory, private_memory


def get_cpu_core_count() -> int:
    result = subprocess.run(["nproc", "--all"], capture_output=True)
    if result.returncode != 0:
        raise Exception("Could not determine number of cores")
    data = result.stdout.decode("utf-8")
    return int(data)


def get_process_average_cpu_utilization(pid: int) -> tuple[bool, float]:
    """
    Get the average CPU utilization of a process.
    Note: This gets the the average CPU utilization over its lifetime, and should
    not be used to get the current CPU utilization.

    Args:
        pid (int): The PID of the process.

    Returns:
        tuple[bool, float]: The first value indicates if it could successfully get the CPU utilization. The second value gives the CPU utilization (in percentage) in case of  a success.
    """
    result = subprocess.run(
        ["ps", "-p", str(pid), "-o", "%cpu", "--no-header"], capture_output=True
    )
    if result.returncode != 0:
        return False, 0
    data = result.stdout.decode("utf-8")
    avg_cpu = float(data)

    # ps doesn't scale CPU usage down based on the number of cores.
    # For example an 8-core CPU could report values between 0% and 800%.
    # We thus need to divide the avg_cpu with the number of cores
    avg_cpu = avg_cpu / get_cpu_core_count()

    return True, avg_cpu


def get_process_information(pid: int) -> dict | None:
    memory_success, shared_memory, private_memory = get_process_memory(pid)

    if not memory_success:
        return None

    result = dict()

    result["shared_memory"] = shared_memory
    result["private_memory"] = private_memory

    return result


def get_command(cwd: str, makefile: str, args: dict):
    command = subprocess.check_output(
        ["make", "-f", makefile, "command"],
        cwd=cwd,
        env=args,
    ).decode("utf-8")
    command = command.strip().split(" ")
    return command


def run_energy_benchmark(
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
    command = get_command(cwd, makefile, args)

    energy_path = os.path.join(
        ROOT,
        "Results",
        f"{benchmark}.{optimizedStr}.{language}.{identifier}.energy.json",
    )
    energy_command = [RAPL_PATH, "--json", energy_path] + command

    description = (
        f"Energy    {benchmark}::{optimizedStr}::{identifier}::{language}".ljust(56)
    )

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
            energy_command,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            cwd=cwd,
            timeout=timeout,
            env=args,
        )


def run_resource_benchmark(
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
    command = get_command(cwd, makefile, args)
    description = (
        f"Resources {benchmark}::{optimizedStr}::{identifier}::{language}".ljust(56)
    )
    resources_path = os.path.join(
        ROOT,
        "Results",
        f"{benchmark}.{optimizedStr}.{language}.{identifier}.resources.json",
    )


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

        # Run resource measurement
        process_data = dict()
        process_data["samples"] = []
        killed = False
        process = subprocess.Popen(
            command,
            shell=False,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            cwd=cwd,
            env=args,
        )

        start = time.time()
        last_measurement = start
        avg_cpu = 0

        while process.poll() is None:
            cpu_success, cpu_percent = get_process_average_cpu_utilization(process.pid)
            if not cpu_success:
                break

            avg_cpu = cpu_percent
            sample = get_process_information(process.pid)

            # If no sample, the process has most likely stopped
            if sample is None:
                break

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
        process_data["cpu"] = avg_cpu
        if killed:
            process_data.samples = None

        with open(resources_path, "a") as file:
            json.dump(process_data, file)
            file.write("\n")


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

    run_energy_benchmark(
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

    run_resource_benchmark(
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
