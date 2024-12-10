use std::{
    collections::HashSet,
    env,
    fs::File,
    io::{BufRead, BufReader, Write},
};

struct Graph {
    vertices: usize,
    incoming: Vec<HashSet<i32>>,
    outgoing: Vec<HashSet<i32>>,
}

impl Graph {
    fn new(path: &str) -> Result<Graph, Box<dyn std::error::Error>> {
        let reader: BufReader<File> = BufReader::new(File::open(path).unwrap());

        let mut vertices: usize = 0;
        let mut incoming: Vec<HashSet<i32>> = Vec::new();
        let mut outgoing: Vec<HashSet<i32>> = Vec::new();

        for line in reader.lines() {
            if line.is_err() {
                continue;
            }
            let line = line.unwrap();

            if line.starts_with('p') {
                let values = line.split(' ').collect::<Vec<&str>>();

                vertices = values[2].parse::<usize>()?;
                incoming = Vec::with_capacity(vertices);
                outgoing = Vec::with_capacity(vertices);

                for _ in 0..vertices {
                    incoming.push(HashSet::new());
                    outgoing.push(HashSet::new());
                }
            } else if line.starts_with('e') || line.starts_with('a') {
                let values = line.split(' ').collect::<Vec<&str>>();

                let v0 = values[1].parse::<i32>()?;
                let v1 = values[2].parse::<i32>()?;

                outgoing.get_mut(v0 as usize).unwrap().insert(v1);
                incoming.get_mut(v1 as usize).unwrap().insert(v0);
            }
        }

        Ok(Graph {
            vertices,
            incoming,
            outgoing,
        })
    }
}

fn page_rank_single(v: i32, graph: &Graph, ranks: &[f32], damping: f32) -> f32 {
    let mut rank = (1f32 - damping) / graph.vertices as f32;

    for u in graph.incoming.get(v as usize).unwrap() {
        let outgoing_rank = *ranks.get(*u as usize).unwrap();
        let outgoing_len = graph.outgoing.get(*u as usize).unwrap().len() as f32;
        rank += damping * outgoing_rank / outgoing_len;
    }

    rank
}

fn page_rank(graph: &Graph, damping: f32, epsilon: f32) -> Vec<f32> {
    let mut ranks: Vec<f32> = Vec::with_capacity(graph.vertices);
    let mut new_ranks: Vec<f32> = Vec::with_capacity(graph.vertices);

    for _ in 0..graph.vertices {
        ranks.push(1f32 / graph.vertices as f32);
        new_ranks.push(1f32 / graph.vertices as f32);
    }

    let mut change = epsilon + 1f32;
    while change > epsilon {
        for v in 0..graph.vertices {
            new_ranks[v] = page_rank_single(v as i32, graph, &ranks, damping);
        }

        change = 0f32;
        for v in 0..graph.vertices {
            change += (ranks[v] - new_ranks[v]).abs();
        }

        for v in 0..graph.vertices {
            ranks[v] = new_ranks[v];
        }
    }

    ranks
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();

    let file = args.get(1).unwrap();
    let out = args.get(2).unwrap();

    let graph = Graph::new(file)?;
    let ranks = page_rank(&graph, 0.85, 1e-4f32);

    let mut file = File::create(out).unwrap();
    for i in 0..ranks.len() {
        let rank = ranks.get(i).unwrap();
        let line = format!("{i} {rank}\n");
        let _ = file.write(line.as_bytes());
    }

    Ok(())
}
