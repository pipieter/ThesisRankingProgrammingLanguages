import argparse
import json
import math
import os
import os.path
import statistics
import numpy as np
from scipy import stats


def read_runtimes(path: str) -> list[float]:
    runtimes = []

    with open(path, "r") as file:
        for line in file.readlines():
            data = json.loads(line)
            runtimes.append(data["runtime_ms"] / 1000)

    return runtimes


def confidence_interval(values: list[float], confidence=0.95):
    mean = np.mean(values)
    standard_error = stats.sem(values)
    critical_t = stats.t.ppf((1 + confidence) / 2, len(values) - 1)

    margin_of_error = critical_t * standard_error
    return mean, margin_of_error


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=str,
        default="./Results",
        help="The path of the JSON files containing the measurements.",
    )

    args = parser.parse_args()
    path = args.path

    if not os.path.exists(path):
        print("Path does not exist.")
        exit(0)

    print("Benchmark,Optimized,Language,Input Size,Mean,Margin Of Error")
    files = sorted(os.listdir(path))
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            continue
        values = read_runtimes(file_path)
        mean, margin_of_error = confidence_interval(values, 0.95)

        identifiers = file.split(".")
        benchmark = identifiers[0]
        optimized = identifiers[1]
        language = identifiers[2]
        input_size = identifiers[3]

        print(
            f"{benchmark},{optimized},{language},{input_size},{mean},{margin_of_error}"
        )
