# Running

```bash
sudo modprobe msr
sudo python3 -m Scripts.generate_input --verbose
sudo python3 -m Scripts.build_rapl --verbose
sudo python3 -m Scripts.build_docker --verbose
sudo docker run -it --privileged thesis
```

The first command is required as the RAPL uses the MSR registers to measure energy usage. The `--priviledged` flag is required to drop the caches.

Running the last command opens a bash shell inside the Docker container.  In order to measure the benchmarks, run:

```bash
python3 -m Scripts.measure
```

You can then summarize the results with:
```bash
python3 -m Scripts.to_csv
```

To copy the results to somewhere:
```bash
sudo docker cp [CONTAINER_ID]:/root/ranking-languages/Results/. Results/.
```

# RAPL

The current RAPL utility tool is the one created by Nicolas van Kempen et al. and can be found here: https://github.com/nicovank/Energy-Languages

# Future notes:

- Python 3.13.0 implements an experimental JIT compiler https://www.python.org/downloads/release/python-3130/ap
- 