import json
import os
import statistics

from Scripts.measure import get_files


ROOT = os.getcwd()


class EnergyData:
    energy: float

    def __init__(self, path: str):
        energy_samples = []
        with open(path, "r") as file:
            for line in file.readlines():
                data = json.loads(line)
                samples = data["energy_samples"]
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
    avg_cores: float

    def __init__(self, path: str) -> None:
        runtimes = []
        avg_shared_memories = []
        avg_private_memories = []
        avg_cores_used = []

        with open(path, "r") as file:
            for line in file.readlines():
                data = json.loads(line)

                # Ignore executions without any samples
                if len(data["samples"]) == 0:
                    continue

                total_runtime = data["total_runtime_ms"] / 1000  # In seconds
                samples = data["samples"]

                parsed = self._parse_samples(samples)
                if parsed is None:
                    continue

                (
                    avg_core_seconds,
                    avg_shared_mem_seconds,
                    avg_private_mem_seconds,
                ) = parsed

                runtimes.append(total_runtime)
                avg_cores_used.append(avg_core_seconds)
                avg_shared_memories.append(avg_shared_mem_seconds)
                avg_private_memories.append(avg_private_mem_seconds)

        self.runtime = 0
        self.avg_cores = 0
        self.avg_shared_memory = 0
        self.avg_private_memory = 0

        if len(runtimes) > 0:
            self.runtime = statistics.mean(runtimes)
            self.avg_cores = statistics.mean(avg_cores_used)
            self.avg_shared_memory = statistics.mean(avg_shared_memories)
            self.avg_private_memory = statistics.mean(avg_private_memories)

    def _parse_samples(self, samples: list[any]) -> None | tuple[float, float, float]:
        if len(samples) == 0:
            return None

        total_core_seconds = 0
        total_shared_mem_seconds = 0
        total_private_memory_seconds = 0
        total_recorded_runtime_seconds = 0

        for sample in samples:
            sample_seconds = sample["runtime_ms"] / 1000

            total_core_seconds += sample["cores"] * sample_seconds
            total_shared_mem_seconds += sample["shared_memory"] * sample_seconds
            total_private_memory_seconds += sample["private_memory"] * sample_seconds

            total_recorded_runtime_seconds += sample_seconds

        avg_core_seconds = total_core_seconds / total_recorded_runtime_seconds
        avg_shared_mem_seconds = (
            total_shared_mem_seconds / total_recorded_runtime_seconds
        )
        avg_private_mem_seconds = (
            total_private_memory_seconds / total_recorded_runtime_seconds
        )

        return avg_core_seconds, avg_shared_mem_seconds, avg_private_mem_seconds


class BenchmarkData:
    benchmark: str
    language: str
    identifier: str

    energy: EnergyData
    resources: ResourceData

    def __init__(self, benchmark: str, language: str, identifier: str) -> None:
        self.benchmark = benchmark
        self.language = language
        self.identifier = identifier

        energy_file = f"{benchmark}.{language}.{identifier}.energy.json"
        resources_file = f"{benchmark}.{language}.{identifier}.resources.json"

        energy_path = os.path.join(ROOT, "Results", energy_file)
        resources_path = os.path.join(ROOT, "Results", resources_file)

        self.energy = EnergyData(energy_path)
        self.resources = ResourceData(resources_path)

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

        return self.language < other.language

    def to_csv_line(self, separator: str = ";") -> str:
        avg_total_memory = (
            self.resources.avg_shared_memory + self.resources.avg_private_memory
        )
        values = [
            self.benchmark,
            self.identifier,
            self.language,
            f"{self.resources.runtime:.4f}",
            f"{self.energy.energy:.4f}",
            f"{self.resources.avg_cores:.4f}",
            f"{avg_total_memory:.4f}",
            f"{self.resources.avg_shared_memory:.4f}",
            f"{self.resources.avg_private_memory:.4f}",
        ]
        return separator.join(values)

    @staticmethod
    def csv_header(separator: str = ";") -> str:
        headers = [
            "Benchmark",
            "Identifier",
            "Language",
            "Runtime (s)",
            "Energy (Ws)",
            "Average cores used",
            "Average total memory (KB)",
            "Average shared memory (KB)",
            "Average private memory (KB)",
        ]
        return separator.join(headers)


if __name__ == "__main__":
    path = os.path.join(ROOT, "Results")

    files = get_files(path)
    files = [file for file in files if file.endswith(".json")]

    energy_files = [file for file in files if file.endswith(".energy.json")]

    data = []
    for energy_file in energy_files:
        benchmark, language, identifier, _, _ = energy_file.split(".")
        data.append(BenchmarkData(benchmark, language, identifier))
    data = sorted(data)

    print(BenchmarkData.csv_header())
    for d in data:
        print(d.to_csv_line())
