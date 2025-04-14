use bumpalo::Bump;

struct Node<'a> {
    left: Option<&'a mut Node<'a>>,
    right: Option<&'a mut Node<'a>>,
}

fn build<'a>(bump: &'a Bump, nodes: i32) -> Option<&'a mut Node<'a>> {
    if nodes == 0i32 {
        return None;
    }

    let nodes_left = nodes / 2;
    let nodes_right = nodes - nodes_left - 1;

    let left = build(bump, nodes_left);
    let right = build(bump, nodes_right);

    Some(bump.alloc(Node { left, right }))
}

fn count(node: Option<&Node>, depth: usize, counts: &mut Vec<i32>) -> () {
    if let Some(node) = node {
        counts[depth] += 1;
        count(node.left.as_deref(), depth + 1, counts);
        count(node.right.as_deref(), depth + 1, counts);
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();

    let nodes = args.get(1).unwrap().parse::<i32>().unwrap();
    let depth = (nodes as f32).log2().ceil() as i32 + 1;

    let bump = Bump::new();
    let node = build(&bump, nodes);
    let mut counts = vec![0i32; depth as usize];

    count(node.as_deref(), 0, &mut counts);

    for i in 0..depth {
        println!("{} {}", i, counts[i as usize]);
    }
}
