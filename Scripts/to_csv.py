import argparse
import json
import os
import statistics

from Scripts.util.util import get_files


ROOT = os.getcwd()


class EnergyData:
    energy: float

    def __init__(self, path: str, outliers_percent: float):
        energy_samples = []
        data = []
        with open(path, "r") as file:
            for line in file.readlines():
                datum = json.loads(line)
                if len(datum["energy_samples"]) == 0:
                    continue
                data.append(datum)
        
        # Remove outliers
        outlier = int(outliers_percent * len(data) / 2)
        data.sort(key=lambda x: x["runtime_ms"])
        data = data[outlier : -outlier - 1]

        for datum in data:
            samples = datum["energy_samples"]
            energy = self._parse_samples(samples)
            energy_samples.append(energy)

        self.energy = 0
        if len(energy_samples) > 0:
            self.energy = statistics.mean(energy_samples)

    def _parse_samples(self, samples: list[any]) -> float:
        energy = 0
        for sample in samples:
            for subsample in sample["energy"]:
                energy += (
                    subsample["pkg"]
                    + subsample["pp0"]
                    + subsample["pp1"]
                    + subsample["dram"]
                )
        return energy


class ResourceData:
    runtime: float
    avg_shared_memory: float
    avg_private_memory: float
    avg_cpu: float

    def __init__(self, path: str, outliers_percent: float) -> None:
        runtimes = []
        avg_cpus = []
        avg_shared_memories = []
        avg_private_memories = []

        data = []

        with open(path, "r") as file:
            for line in file.readlines():
                datum = json.loads(line)
                if len(datum["samples"]) > 0:
                    data.append(datum)

        # Remove outliers
        outlier = int(outliers_percent * len(data) / 2)
        data.sort(key=lambda x: x["total_runtime_ms"])
        data = data[outlier : -outlier - 1]

        # Parse samples
        for datum in data:
            runtime = datum["total_runtime_ms"] / 1000  # In seconds
            cpu = datum["cpu"]
            samples = datum["samples"]
            parsed = self._parse_samples(samples)

            if samples is None:
                continue

            avg_shared_mem, avg_private_mem = parsed

            runtimes.append(runtime)
            avg_cpus.append(cpu)
            avg_shared_memories.append(avg_shared_mem)
            avg_private_memories.append(avg_private_mem)

        self.runtime = 0
        self.avg_cpu = 0
        self.avg_shared_memory = 0
        self.avg_private_memory = 0

        if len(runtimes) > 0:
            self.runtime = statistics.mean(runtimes)
            self.avg_cpu = statistics.mean(avg_cpus)
            self.avg_shared_memory = statistics.mean(avg_shared_memories)
            self.avg_private_memory = statistics.mean(avg_private_memories)

    def _parse_samples(self, samples: list[any]) -> None | tuple[float, float]:
        if len(samples) == 0:
            return None

        total_shared_mem_seconds = 0
        total_private_memory_seconds = 0
        total_recorded_runtime_seconds = 0

        for sample in samples:
            sample_seconds = sample["runtime_ms"] / 1000

            total_shared_mem_seconds += sample["shared_memory"] * sample_seconds
            total_private_memory_seconds += sample["private_memory"] * sample_seconds

            total_recorded_runtime_seconds += sample_seconds

        avg_shared_mem_seconds = (
            total_shared_mem_seconds / total_recorded_runtime_seconds
        )
        avg_private_mem_seconds = (
            total_private_memory_seconds / total_recorded_runtime_seconds
        )

        return avg_shared_mem_seconds, avg_private_mem_seconds


class BenchmarkData:
    benchmark: str
    optimized: str
    language: str
    identifier: str

    energy: EnergyData
    resources: ResourceData

    def __init__(
        self,
        benchmark: str,
        optimized: str,
        language: str,
        identifier: str,
        outliers_threshold,
    ) -> None:
        self.benchmark = benchmark
        self.optimized = optimized
        self.language = language
        self.identifier = identifier

        energy_file = f"{benchmark}.{optimized}.{language}.{identifier}.energy.json"
        resources_file = (
            f"{benchmark}.{optimized}.{language}.{identifier}.resources.json"
        )

        energy_path = os.path.join(ROOT, "Results", energy_file)
        resources_path = os.path.join(ROOT, "Results", resources_file)

        self.energy = EnergyData(energy_path, outliers_threshold)
        self.resources = ResourceData(resources_path, outliers_threshold)

    def __lt__(self, other) -> bool:
        if not isinstance(other, BenchmarkData):
            return False

        if self.benchmark != other.benchmark:
            return self.benchmark < other.benchmark

        if self.identifier != other.identifier:
            # Check if value can be an integer
            try:
                self_int = int(self.identifier, base=10)
                other_int = int(other.identifier, base=10)
                return self_int < other_int
            except:
                return self.identifier < other.identifier

        if self.language != other.language:
            return self.language < other.language

        # Unoptimized first
        return self.optimized > other.optimized

    def to_csv_line(self, separator: str = ";") -> str:
        avg_total_memory = (
            self.resources.avg_shared_memory + self.resources.avg_private_memory
        )
        values = [
            self.benchmark,
            self.optimized,
            self.identifier,
            self.language,
            f"{self.resources.runtime:.4f}",
            f"{self.energy.energy:.4f}",
            f"{self.resources.avg_cpu:.4f}",
            f"{avg_total_memory:.4f}",
            f"{self.resources.avg_shared_memory:.4f}",
            f"{self.resources.avg_private_memory:.4f}",
        ]
        return separator.join(values)

    @staticmethod
    def csv_header(separator: str = ";") -> str:
        headers = [
            "Benchmark",
            "Optimized",
            "Identifier",
            "Language",
            "Runtime (s)",
            "Energy (Ws)",
            "Average CPU utilization (%)",
            "Average total memory (KB)",
            "Average shared memory (KB)",
            "Average private memory (KB)",
        ]
        return separator.join(headers)


if __name__ == "__main__":
    path = os.path.join(ROOT, "Results")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outliers",
        type=float,
        help="Threshold for which outliers to remove based on runtime. For example, a value of 0.2 would remove 10% bottom and 10% top outliers",
        default=0.0,
    )

    args = parser.parse_args()
    outliers_threshold = args.outliers

    files = get_files(path)
    files = [file for file in files if file.endswith(".json")]

    energy_files = [file for file in files if file.endswith(".energy.json")]

    data = []
    for energy_file in energy_files:
        benchmark, optimized, language, identifier, _, _ = energy_file.split(".")
        data.append(
            BenchmarkData(
                benchmark, optimized, language, identifier, outliers_threshold
            )
        )
    data = sorted(data)

    print(BenchmarkData.csv_header())
    for d in data:
        print(d.to_csv_line())
