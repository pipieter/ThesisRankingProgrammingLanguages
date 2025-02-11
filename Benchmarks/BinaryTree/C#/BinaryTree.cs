public class Node
{
    public Node left;
    public Node right;

    public Node(Node left, Node right)
    {
        this.left = left;
        this.right = right;
    }
}

public static class BinaryTree
{
    public static Node Build(int nodes)
    {
        if (nodes == 0)
        {
            return null;
        }

        int nodesLeft = nodes / 2;
        int nodesRight = nodes - nodesLeft - 1;

        Node left = Build(nodesLeft);
        Node right = Build(nodesRight);

        return new Node(left, right);
    }

    public static void Count(Node node, int depth, int[] counts)
    {
        if (node == null)
            return;

        counts[depth] += 1;
        Count(node.left, depth + 1, counts);
        Count(node.right, depth + 1, counts);
    }

    public static void Main(string[] args)
    {
        int nodes = int.Parse(args[0]);
        int depth = (int)System.Math.Ceiling(System.Math.Log((double)nodes) / System.Math.Log(2.0));

        Node node = Build(nodes);
        int[] counts = new int[depth];

        Count(node, 0, counts);

        for (int d = 0; d < depth; d++)
        {
            System.Console.WriteLine($"{d} {counts[d]}");
        }
    }
}