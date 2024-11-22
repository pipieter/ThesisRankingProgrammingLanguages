## File format

The first line of the .graph file is the amount of nodes within the graph. Nodes have an id within [0,amount[.

All subsequent lines are a directed edge "a b" where a points to b.

## Implementation specifics

- We use arrays when possible, though this makes the code less generic.

## Notes

- C++'s unordered_map is very slow