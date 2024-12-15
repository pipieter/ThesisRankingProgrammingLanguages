namespace TriangleCount;

class Graph
{
    public HashSet<int>[] Edges { get; private set; } = [];
    public int NVertices { get { return Edges.Length; } }

    public Graph(string path)
    {
        using StreamReader reader = new(path);

        string? line = reader.ReadLine();
        while (line != null)
        {
            if (line.StartsWith('p'))
            {
                string[] values = line.Split(' ');
                int vertices = int.Parse(values[2]);

                Edges = new HashSet<int>[vertices];
                for (int i = 0; i < vertices; i++)
                {
                    Edges[i] = [];
                }
            }
            else if (line.StartsWith('a') || line.StartsWith('e'))
            {
                string[] values = line.Split(' ');
                int a = int.Parse(values[1]);
                int b = int.Parse(values[2]);

                if (a != b)
                {
                    Edges[a].Add(b);
                    Edges[b].Add(a);
                }
            }

            line = reader.ReadLine();
        }
    }
}

class TriangleCounter
{
    public static int TriangleCount_single(Graph graph, int a, int b)
    {
        if (a >= b) return 0;

        HashSet<int> edgesA = graph.Edges[a];
        HashSet<int> edgesB = graph.Edges[b];

        return edgesA.Intersect(edgesB).Count();
    }

    public static int TriangleCount(Graph graph)
    {
        int count = 0;
        for (int a = 0; a < graph.NVertices; a++)
        {
            for (int b = a + 1; b < graph.NVertices; b++)
            {
                count += TriangleCount_single(graph, a, b);
            }
        }

        return count;
    }

    public static void Main(string[] args)
    {
        string file = args[0];

        var graph = new Graph(file);
        var count = TriangleCount(graph);

        System.Console.WriteLine(count);
    }
}