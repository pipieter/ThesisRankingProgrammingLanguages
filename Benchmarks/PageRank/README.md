# PageRank

Calculate the PageRank weights of the nodes within a group. Requires a [DIMACS graph file](https://www.diag.uniroma1.it//challenge9/format.shtml#graph) as input graph and writes the results to a given output file with format `[node] [weight]`.

The measured graphs were generated using [Graph500's Kronecker graph algorithm](https://github.com/pipieter/graph-generator).

Usage: `./program [input path] [output path]`