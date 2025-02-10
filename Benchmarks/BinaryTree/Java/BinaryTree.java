public class BinaryTree {
    public static Node build(int nodes) {
        if (nodes == 0) {
            return null;
        }

        int nodesLeft = nodes / 2;
        int nodesRight = nodes - nodesLeft - 1;

        Node left = build(nodesLeft);
        Node right = build(nodesRight);

        return new Node(left, right);
    }

    public static void count(Node tree, int depth, int[] target) {
        if (tree == null) {
            return;
        }

        target[depth] += 1;
        count(tree.left, depth + 1, target);
        count(tree.right, depth + 1, target);
    }

    public static void main(String[] args) {
        int nodes = Integer.parseInt(args[0]);
        int depth = (int) Math.ceil((double) Math.log(nodes) / (double) Math.log(2.0));

        Node tree = build(nodes);
        int[] counts = new int[depth];

        count(tree, 0, counts);

        for (int i = 0; i < depth; i++) {
            System.out.format("%d %d%n", i, counts[i]);
        }
    }
}