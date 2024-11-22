import statistics
import subprocess
import time

import psutil


def run(command: str) -> None:
    n = 10
    results = []

    for _ in range(n):
        peak_memory = 0
        start = time.time()

        process = subprocess.Popen(command, stdout=None, stderr=None, shell=False)
        while process.poll() == None:
            try:
                info = psutil.Process(process.pid)
                memory = info.memory_info()[0]
                peak_memory = max(peak_memory, memory)
            except:
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
    except:
        mean_time = results[0][0]
        mean_memory = results[0][1]

    return mean_time, mean_memory


SIZES = [1024, 2048, 4096, 8192]

processes = [
    ("Python", "python ./python/pagerank.py FILE temp"),
    ("Java", "java ./java/PageRank.java FILE temp"),
    ("C#", "./csharp/build/csharp FILE temp"),
    ("C++", "./cpp/pagerank FILE temp"),
    ("Rust", "./rust/target/release/rust FILE temp"),
]

if __name__ == "__main__":
    for size in SIZES:
        file = f"./out.{size}.graph"
        for process in processes:
            language, command = process
            command = command.replace("FILE", file)

            mean_time, mean_memory = run(command)
            print(f"{language};{size};{mean_time};{mean_memory}")
