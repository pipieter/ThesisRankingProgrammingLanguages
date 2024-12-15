use std::{
    collections::HashSet,
    env,
    error::Error,
    fs::File,
    io::{BufRead, BufReader},
};

struct Graph {
    vertices: usize,
    edges: Vec<HashSet<i32>>,
}

impl Graph {
    fn new(path: &str) -> Result<Graph, Box<dyn Error>> {
        let reader: BufReader<File> = BufReader::new(File::open(path).unwrap());

        let mut vertices: usize = 0;
        let mut edges: Vec<HashSet<i32>> = Vec::new();

        for line in reader.lines() {
            if line.is_err() {
                continue;
            }
            let line = line.unwrap();

            if line.starts_with('p') {
                let values = line.split(' ').collect::<Vec<&str>>();

                vertices = values[2].parse::<usize>()?;
                edges = Vec::with_capacity(vertices);

                for _ in 0..vertices {
                    edges.push(HashSet::new());
                }
            } else if line.starts_with('e') || line.starts_with('a') {
                let values = line.split(' ').collect::<Vec<&str>>();

                let v0 = values[1].parse::<i32>()?;
                let v1 = values[2].parse::<i32>()?;

                if v0 != v1 {
                    edges.get_mut(v0 as usize).unwrap().insert(v1);
                    edges.get_mut(v1 as usize).unwrap().insert(v0);
                }
            }
        }

        Ok(Graph { vertices, edges })
    }
}

fn triangle_count_single(graph: &Graph, a: i32, b: i32) -> i32 {
    if a >= b {
        return 0i32;
    }

    let edges_a = graph.edges.get(a as usize).unwrap();
    let edges_b = graph.edges.get(b as usize).unwrap();

    let size = edges_a.intersection(edges_b).count();

    size as i32
}

fn triangle_count(graph: &Graph) -> i32 {
    let mut count = 0;

    for a in 0..graph.vertices {
        for b in a + 1..graph.vertices {
            count += triangle_count_single(graph, a as i32, b as i32);
        }
    }

    count
}

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();

    let file = args.get(1).unwrap();
    let graph = Graph::new(file)?;

    let count = triangle_count(&graph);

    println!("{}", count);

    Ok(())
}
