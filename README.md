# Running

```bash
sudo modprobe msr
sudo python3 -m Scripts.setup --verbose 1
# sudo docker rm thesis
# sudo docker run -it --privileged --name thesis thesis .
sudo docker run -it --privileged thesis .
```

The first command is required as the RAPL uses the MSR registers to measure energy usage. The `--priviledged` flag is required to drop the caches.

To copy the results to somewhere:
```bash
sudo docker cp [CONTAINER_ID]:/root/ranking-languages/Results/. Results/.
```

# RAPL

The current RAPL utility tool is the one created by Nicolas van Kempen et al. and can be found here: https://github.com/nicovank/Energy-Languages

# Future notes:

- Python 3.13.0 implements an experimental JIT compiler https://www.python.org/downloads/release/python-3130/ap
- 