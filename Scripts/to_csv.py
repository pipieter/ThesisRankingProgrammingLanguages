import argparse
import json
import os
import statistics

from Scripts.util.util import get_files


ROOT = os.getcwd()


class Data:
    runtime_ms: float

    energy: float
    avg_shared_memory: float
    avg_private_memory: float
    avg_swapped_memory: float
    avg_cpu: float
    cpu_count: int

    hw_instructions: int
    hw_cpu_cycles: int
    hw_cache_miss_rate: float
    hw_branch_miss_rate: float

    def __init__(self, path: str):
        runtime_values = []
        energy_values = []
        avg_shared_memory_values = []
        avg_private_memory_values = []
        avg_swapped_memory_values = []
        avg_cpu_values = []
        cpu_count_values = []

        hw_instructions_values = []
        hw_cpu_cycles_values = []
        hw_cache_miss_rates_values = []
        hw_branch_miss_rates_values = []

        data = []

        # Read json
        with open(path, "r") as file:
            for line in file.readlines():
                datum = json.loads(line)

                # Only add samples if there:
                # - There is at least one energy sample
                # - There is at least one process sample
                # - The average cpu usage is larger than 0

                if len(datum["energy_samples"]) == 0:
                    continue

                if len(datum["process"]["samples"]) == 0:
                    continue

                if datum["process"]["avg_cpu"] == 0:
                    continue

                data.append(datum)

        # Parse runtimes
        for datum in data:
            runtime_values.append(datum["runtime_ms"])

        # Parse energy values
        for datum in data:
            energy_values.append(self._parse_energy_samples(datum["energy_samples"]))

        # Parse process data
        for datum in data:
            (
                avg_shared_memory_value,
                avg_private_memory_value,
                avg_swapped_memory_value,
            ) = self._parse_process_memory_samples(datum["process"]["samples"])
            cpu_count_value = datum["process"]["cpu_count"]
            avg_cpu_value = datum["process"]["avg_cpu"]

            avg_shared_memory_values.append(avg_shared_memory_value)
            avg_private_memory_values.append(avg_private_memory_value)
            avg_swapped_memory_values.append(avg_swapped_memory_value)
            cpu_count_values.append(cpu_count_value)
            avg_cpu_values.append(avg_cpu_value)

            hw_instructions_values.append(datum["counters"]["PERF_COUNT_HW_INSTRUCTIONS"])
            hw_cpu_cycles_values.append(datum["counters"]["PERF_COUNT_HW_CPU_CYCLES"])
            hw_cache_miss_rates_values.append(
                datum["counters"]["PERF_COUNT_HW_CACHE_MISSES"]
                / datum["counters"]["PERF_COUNT_HW_CACHE_REFERENCES"]
            )
            hw_branch_miss_rates_values.append(
                datum["counters"]["PERF_COUNT_HW_BRANCH_MISSES"]
                / datum["counters"]["PERF_COUNT_HW_BRANCH_INSTRUCTIONS"]
            )

        # Average results
        self.runtime_ms = self._average(runtime_values)
        self.energy = self._average(energy_values)
        self.avg_shared_memory = self._average(avg_shared_memory_values)
        self.avg_private_memory = self._average(avg_private_memory_values)
        self.avg_swapped_memory = self._average(avg_swapped_memory_values)
        self.avg_cpu = self._average(avg_cpu_values)
        self.cpu_count = self._average(cpu_count_values)
        
        self.hw_instructions = int(self._average(hw_instructions_values))
        self.hw_cpu_cycles = int(self._average(hw_cpu_cycles_values))
        self.hw_cache_miss_rate = self._average(hw_cache_miss_rates_values)
        self.hw_branch_miss_rate = self._average(hw_branch_miss_rates_values)

    def _average(self, values: list[float]) -> float:
        if len(values) == 0:
            return 0.0

        return statistics.mean(values)

    def _parse_energy_samples(self, samples: list[any]) -> float:
        energy = 0
        for sample in samples:
            for subsample in sample["energy"]:
                energy += (
                    # pp0 and pp1 are already included in pkg
                    subsample["pkg"]
                    # + subsample["pp0"]
                    # + subsample["pp1"]
                    + subsample["dram"]
                )
        return energy

    def _parse_process_memory_samples(self, samples: list[any]) -> tuple[float, float]:
        total_duration = 0
        total_shared_memory = 0
        total_private_memory = 0
        total_swapped_memory = 0

        for sample in samples:
            total_duration += sample["duration_ms"]
            total_shared_memory += sample["duration_ms"] * sample["shared_memory"]
            total_private_memory += sample["duration_ms"] * sample["private_memory"]
            total_swapped_memory += sample["duration_ms"] * sample["swapped_memory"]

        return (
            total_shared_memory / total_duration,
            total_private_memory / total_duration,
            total_swapped_memory / total_duration,
        )


class BenchmarkData:
    benchmark: str
    optimized: str
    language: str
    identifier: str

    data: Data

    def __init__(
        self,
        benchmark: str,
        optimized: str,
        language: str,
        identifier: str,
    ) -> None:
        self.benchmark = benchmark
        self.optimized = optimized
        self.language = language
        self.identifier = identifier

        file = f"{benchmark}.{optimized}.{language}.{identifier}.json"
        path = os.path.join(ROOT, "Results", file)

        self.data = Data(path)

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
        runtime_s = self.data.runtime_ms / 1000
        if self.data.cpu_count == 0:
            avg_cpu_normalized = 0
        else:
            avg_cpu_normalized = self.data.avg_cpu / self.data.cpu_count

        avg_total_memory = self.data.avg_shared_memory + self.data.avg_private_memory

        values = [
            self.benchmark,
            self.optimized,
            self.identifier,
            self.language,
            f"{runtime_s:.4f}",
            f"{self.data.energy:.4f}",
            f"{avg_cpu_normalized:.4f}",
            f"{avg_total_memory:.4f}",
            f"{self.data.avg_shared_memory:.4f}",
            f"{self.data.avg_private_memory:.4f}",
            f"{self.data.avg_swapped_memory:.4f}",
            f"{self.data.hw_cpu_cycles}",
            f"{self.data.hw_instructions}",
            f"{self.data.hw_cache_miss_rate}",
            f"{self.data.hw_branch_miss_rate}"
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
            "Average swapped memory (KB)",
            "CPU cycles",
            "Instruction count",
            "Cache miss rate",
            "Branch miss rate"
        ]
        return separator.join(headers)


if __name__ == "__main__":
    path = os.path.join(ROOT, "Results")

    files = get_files(path)
    files = [file for file in files if file.endswith(".json")]

    data = []
    for file in files:
        benchmark, optimized, language, identifier, _ = file.split(".")
        data.append(BenchmarkData(benchmark, optimized, language, identifier))
    data = sorted(data)

    print(BenchmarkData.csv_header())
    for d in data:
        print(d.to_csv_line())
