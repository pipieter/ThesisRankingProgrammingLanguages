use std::env;

use rand::Rng;

struct Graph {
    vertices: usize,
    incoming: Vec<Vec<i32>>,
    outgoing: Vec<Vec<i32>>,
}

impl Graph {
    fn from_random(vertices: usize, density: f32) -> Graph {
        let mut rng = rand::rng();
        let mut incoming: Vec<Vec<i32>> = Vec::with_capacity(vertices);
        let mut outgoing: Vec<Vec<i32>> = Vec::with_capacity(vertices);
        for _ in 0..vertices {
            incoming.push(Vec::new());
            outgoing.push(Vec::new());
        }

        for i in 0..vertices {
            for j in 0..vertices {
                let vertex: f32 = rng.random();
                if i != j && vertex < density {
                    incoming[i].push(j as i32);
                    outgoing[j].push(i as i32);
                }
            }
        }

        Graph {
            vertices,
            incoming,
            outgoing,
        }
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
        new_ranks = (0..graph.vertices)
            .map(|v| page_rank_single(v as i32, graph, &ranks, damping))
            .collect();
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

    let vertices = args.get(1).unwrap().parse::<usize>()?;
    let density = args.get(2).unwrap().parse::<f32>()?;
    let iterations = args.get(3).unwrap().parse::<usize>()?;

    let graph = Graph::from_random(vertices, density);
    let mut total_sum = 0.0f32;

    for i in 0..iterations {
        let ranks = page_rank(&graph, 0.85 + (i as f32) / 1000.0f32, 1e-4f32);
        total_sum += ranks.iter().sum::<f32>();
    }

    println!("{}", total_sum);

    Ok(())
}
