import dataclasses
import json
import os
import statistics

from Scripts.measure import get_files


ROOT = os.getcwd()


@dataclasses.dataclass
class EnergyData:
    energy: float


@dataclasses.dataclass
class ResourceData:
    runtime: float
    avg_shared_memory: float
    avg_private_memory: float


def get_energy_data(energy_file_path: str) -> EnergyData:
    with open(energy_file_path, "r") as file:
        energy_samples = []
        for line in file.readlines():
            data = json.loads(line)
            samples = data["energy_samples"]
            energy = 0
            for sample in samples:
                for subsample in sample["energy"]:
                    energy += (
                        subsample["pkg"]
                        + subsample["pp0"]
                        + subsample["pp1"]
                        + subsample["dram"]
                    )
            energy_samples.append(energy)

    energy = 0
    if len(energy_samples) > 0:
        energy = statistics.mean(energy_samples)

    return EnergyData(energy=energy)


def get_resources_data(resources_file_path: str) -> ResourceData:
    with open(resources_file_path, "r") as file:
        runtimes = []
        avg_shared_memories = []
        avg_private_memories = []

        for line in file.readlines():
            data = json.loads(line)
            runtime = data["total_runtime_ms"] / 1000  # In seconds

            shared_memory = 0
            private_memory = 0
            for mem in data["samples"]:
                # In seconds
                shared_memory += mem["shared_memory"] * \
                    mem["runtime_ms"] / 1000
                private_memory += mem["private_memory"] * \
                    mem["runtime_ms"] / 1000

            avg_shared_memory = shared_memory / runtime
            avg_private_memory = private_memory / runtime

            runtimes.append(runtime)
            avg_shared_memories.append(avg_shared_memory)
            avg_private_memories.append(avg_private_memory)

    if len(runtimes) == 0:
        return ResourceData(0, 0, 0)

    runtime = statistics.mean(runtimes)
    avg_shared_memory = statistics.mean(avg_shared_memories)
    avg_private_memory = statistics.mean(avg_private_memories)

    return ResourceData(
        runtime=runtime,
        avg_shared_memory=avg_shared_memory,
        avg_private_memory=avg_private_memory,
    )


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

        self.energy = get_energy_data(energy_path)
        self.resources = get_resources_data(resources_path)

    def __lt__(self, other) -> bool:
        if not isinstance(other, BenchmarkData):
            return False

        if self.benchmark != other.benchmark:
            return self.benchmark < other.benchmark

        if self.identifier != other.identifier:
            return self.benchmark < other.identifier

        return self.language < other.language

    def to_csv_line(self, separator: str = ";") -> str:
        return f"{self.benchmark}{separator}{self.identifier}{separator}{self.language}{separator}{self.energy.energy:.4f}{separator}{self.resources.runtime:.4f}{separator}{self.resources.avg_private_memory:.4f}{separator}{self.resources.avg_shared_memory:.4f}"

    @staticmethod
    def csv_header(separator: str = ";") -> str:
        return f"Benchmark{separator}Identifier{separator}Language{separator}Energy (Ws){separator}Runtime (s){separator}Average private memory (KB){separator}Average shared memory (KB)"


def parse():
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


if __name__ == "__main__":
    parse()
