import math
import statistics
import psutil
import subprocess
import time


def run(command: str) -> None:
    n = 10
    results = []

    for _ in range(n):
        peak_memory = 0
        start = time.time()

        process = subprocess.Popen(command, stdout=None, stderr=None, shell=False)
        while process.poll() is None:
            try:
                info = psutil.Process(process.pid)
                memory = info.memory_info()[0]
                peak_memory = max(peak_memory, memory)
            except BaseException:
                ...
            time.sleep(0.001)
        end = time.time()

        delta = end - start
        results.append((delta, peak_memory))

    results.sort(key=lambda x: x[0])

    # Remove outliers
    results = results[2:-2]

    times = [result[0] for result in results]
    memory = [result[1] for result in results]

    try:
        mean_time = statistics.fmean(times)
        mean_memory = statistics.fmean(memory)
    except BaseException:
        mean_time = results[0][0]
        mean_memory = results[0][1]

    return mean_time, mean_memory


SIZES = [4096, 8192, 16384, 32768, 65536, 131072, 262144]
MEMORY_SIZES = [128000]  # [64000, 128000, 256000, 512000]
FILE = "./out.txt"

MEMORY = 640_000

processes = [
    ("Python", "python ./python/merge_sort.py FILE ./sorted.py.txt MEMORY"),
    ("Java", "java ./java/MergeSort.java FILE ./sorted.java.txt MEMORY"),
    ("C#", "./csharp/build/csharp FILE ./sorted.cs.txt MEMORY"),
    ("C++", "./cpp/merge_sort FILE ./sorted.cpp.txt MEMORY"),
    ("Rust", "./rust/target/release/rust FILE ./sorted.rs.txt MEMORY"),
]

if __name__ == "__main__":
    for size in SIZES:
        file = f"out.{size}.txt"
        for memory in MEMORY_SIZES:
            for process in processes:
                language, command = process
                command = command.replace("FILE", file)
                command = command.replace("MEMORY", str(memory))

                mean_time, mean_memory = run(command)
                print(f"{language};{size};{memory};{mean_time};{mean_memory}")
