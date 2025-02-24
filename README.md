# Cloning

This repository can be pulled with:

```bash
git clone --recursive
```

This will include the RAPL tool repository.

# Requirements

The matrix multiplication algorithm makes use of OpenBLAS for matrix multiplication, which can be installed using 

```bash
sudo apt-get install libopenblas-dev
```

This is not needed if the docker container is used.

# Building

All command blocks are assumed they are first executed in the root directory.

## Generating input

Input files can be generated using

```bash
sudo python3 -m Scripts.generate_input --verbose
```

This will generate random string files for MergeSort. Graph files are currently generated using an external tool.

## Building RAPL

RAPL makes use of the Intel's model-specific registries (MSR). These need to be enabled for RAPL to work, which requires sudo permissions. Note that the CMake commands also require sudo, to build, as building RAPL requires access to the MSRs.

```bash
mkdir RAPL/build
cd RAPL/build
sudo modprobe msr
sudo cmake ..
sudo cmake --build .
cd ../..
```

## Building Docker

The Docker can be build using teh following command:

```bash
cd Docker
sudo docker build -f Dockerfile --tag thesis ..
cd ..
```

# Running

The Docker container can the following command. The `--priviledged` flag is required to drop the caches and to access the MSRs.

```bash
sudo docker run -it --privileged thesis
```

Running the last command opens a bash shell inside the Docker container. Inside the container, to run the benchmarks, do:

```bash
python3 -m Scripts.compile      # Compile the benchmarks
python3 -m Scripts.measure      # Measure the benchmarks
python3 -m Scripts.to_csv       # Summarize the benchmarks
```

To copy the results to somewhere:

```bash
sudo docker cp [CONTAINER_ID]:/root/ranking-languages/Results/. Results/.
```

# RAPL

The current RAPL utility tool is based on the one created by [Nicolas van Kempen et al](https://github.com/nicovank/Energy-Languages), and can be found here: https://github.com/pipieter/Thesis-RAPL.

# To do

| Benchmark    | C#  | C++ | Java | Python | Rust |
| ------------ | --- | --- | ---- | ------ | ---- |
| Binary trees | -   | O   | -    | -      | -    |
| IONumber     | -   | -   | -    | -      | -    |
| MatrixMult   | -   | O   | -    | O      | O    |
| MergeSort    | O   | O   | O    | -      | O    |
| PageRank     | O   | O   | O    | O      | -    |
