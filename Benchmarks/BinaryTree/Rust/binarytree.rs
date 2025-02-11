struct Node {
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

impl Node {
    fn new(left: Option<Box<Node>>, right: Option<Box<Node>>) -> Self {
        Self { left, right }
    }
}

fn build(nodes: i32) -> Option<Box<Node>> {
    if nodes == 0i32 {
        return None;
    }

    let nodes_left = nodes / 2;
    let nodes_right = nodes - nodes_left - 1;

    let left = build(nodes_left);
    let right = build(nodes_right);

    Some(Box::new(Node::new(left, right)))
}

fn count(node: Option<Box<Node>>, depth: usize, counts: &mut Vec<i32>) -> () {
    if let Some(node) = node {
        counts[depth] += 1;
        count(node.left, depth + 1, counts);
        count(node.right, depth + 1, counts);
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();

    let nodes = args.get(1).unwrap().parse::<i32>().unwrap();
    let depth = (nodes as f32).log2().ceil() as i32 + 1;

    let node = build(nodes);
    let mut counts = vec![0i32; depth as usize];

    count(node, 0, &mut counts);

    for i in 0..depth {
        println!("{} {}", i, counts[i as usize]);
    }
}
