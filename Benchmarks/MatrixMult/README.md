# Matrix Multiplication

Blocked matrix multiplication based on [Using Blocking to Increase Temporal Locality](https://csapp.cs.cmu.edu/2e/waside/waside-blocking.pdf). The ordering of inner loops is determined by optimal performance for GCC.

The programs expect a N*N matrix text file with the format below. The program writes the multiplied matrix to an output file in the same format.

```
[dimension N]
[value at 0 0]
[value at 0 1]
[value at 0 2]
...
[value at 0 (N-1)]
[value at 1 0]
[value at 1 1]
...
[value at (N-1) (N-2)]
[value at (N-1) (N-1)]
```

Usage: `./program [first matrix path] [second matrix path] [output path]`

Alternate, optimized versions for C++, Python, and Rust were written to use external libraries. These libraries are OpenBLAS for C++, NumPy for Python, and rulinalg for Rust. These programs work the same as the non-optimized versions. For C# an optimized version was also written with OpenBlas using `System.Runtime.InteropServices`.

The largest amount of time for the optimized was spent reading the input file. As such, separate programs using zero-filled matrices were also written for the languages with an optimized versions.