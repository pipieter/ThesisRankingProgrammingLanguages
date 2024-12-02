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
    avg_memory: float


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
        avg_memories = []
        runtimes = []
        for line in file.readlines():
            data = json.loads(line)
            runtime = data["total_runtime_ms"] / 1000  # In seconds
            memory = sum(
                [mem["memory"] * mem["runtime_ms"] /
                    1000 for mem in data["samples"]]
            )
            avg_memory = memory / runtime

            runtimes.append(runtime)
            avg_memories.append(avg_memory)

    if len(avg_memories) == 0:
        return ResourceData(0, 0)

    avg_memory = statistics.mean(avg_memories)
    runtime = statistics.mean(runtimes)

    return ResourceData(runtime=runtime, avg_memory=avg_memory)


def parse():
    path = os.path.join(ROOT, "Results")

    files = get_files(path)
    files = [file for file in files if file.endswith(".json")]

    energy_files = [file for file in files if file.endswith(".energy.json")]
    resources_files = [
        file for file in files if file.endswith(".resources.json")]

    for energy_file in energy_files:
        benchmark, language, identifier, _, _ = energy_file.split(".")
        file_path = os.path.join(path, energy_file)
        energy = get_energy_data(file_path)
        print(f"{benchmark};{language};{identifier};{energy.energy:.4f}")

    print()

    for resources_file in resources_files:
        benchmark, language, identifier, _, _ = resources_file.split(".")
        file_path = os.path.join(path, resources_file)
        resources = get_resources_data(file_path)
        print(
            f"{benchmark};{language};{identifier};{resources.runtime:.4f};{resources.avg_memory:.4f}"
        )


if __name__ == "__main__":
    parse()
