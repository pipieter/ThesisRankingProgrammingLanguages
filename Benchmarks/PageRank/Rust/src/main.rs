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
    fn new(path: &str) -> Graph {
        let mut reader: BufReader<File> = BufReader::new(File::open(path).unwrap());

        let mut line = String::new();
        let _ = reader.read_line(&mut line);
        line = line.trim().to_string();

        let vertices = line.parse::<usize>().unwrap();
        let mut incoming: Vec<HashSet<i32>> = Vec::with_capacity(vertices);
        let mut outgoing: Vec<HashSet<i32>> = Vec::with_capacity(vertices);

        for _ in 0..vertices {
            incoming.push(HashSet::<i32>::new());
            outgoing.push(HashSet::<i32>::new());
        }

        for line in reader.lines() {
            if line.is_err() {
                continue;
            }

            let line = line.unwrap().trim().to_string();
            let values: Vec<&str> = line.split(' ').collect();
            let a = values[0].parse::<i32>().unwrap();
            let b = values[1].parse::<i32>().unwrap();

            outgoing.get_mut(a as usize).unwrap().insert(b);
            incoming.get_mut(b as usize).unwrap().insert(a);
        }

        Graph {
            vertices,
            incoming,
            outgoing,
        }
    }
}

fn page_rank_single(v: i32, graph: &Graph, ranks: &Vec<f32>, damping: f32) -> f32 {
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
            change += (ranks[v] - new_ranks[v]).abs() as f32;
        }

        for v in 0..graph.vertices {
            ranks[v] = new_ranks[v];
        }
    }

    ranks
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file = args.get(1).unwrap();
    let out = args.get(2).unwrap();

    let graph = Graph::new(file);
    let ranks = page_rank(&graph, 0.85, 1e-4f32);

    let mut file = File::create(out).unwrap();
    for i in 0..ranks.len() {
        let rank = ranks.get(i).unwrap();
        let line = format!("{i} {rank}\n");
        let _ = file.write(line.as_bytes());
    }
}
