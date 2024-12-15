namespace PageRankArray;

class Graph
{
    public List<int>[] Outgoing { get; private set; } = [];
    public List<int>[] Incoming { get; private set; } = [];
    public int NVertices { get; private set; } = 0;

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

                NVertices = vertices;
                Outgoing = new List<int>[vertices];
                Incoming = new List<int>[vertices];

                for (int i = 0; i < vertices; i++)
                {
                    Outgoing[i] = [];
                    Incoming[i] = [];
                }
            }
            else if (line.StartsWith('a') || line.StartsWith('e'))
            {
                string[] values = line.Split(' ');
                int a = int.Parse(values[1]);
                int b = int.Parse(values[2]);

                Outgoing[a].Add(b);
                Incoming[b].Add(a);
            }

            line = reader.ReadLine();
        }
    }
}

class PageRanker
{
    public static float PageRank_single(int v, Graph graph, float[] ranks, float damping)
    {
        float rank = (1.0f - damping) / graph.NVertices;

        foreach (int u in graph.Incoming[v])
            rank += damping * ranks[u] / graph.Outgoing[u].Count;

        return rank;
    }

    public static float[] PageRank(Graph graph, float damping, float epsilon = 1e-4f)
    {
        float[] ranks = new float[graph.NVertices];
        float[] newRanks = new float[graph.NVertices];

        for (int v = 0; v < graph.NVertices; v++)
        {
            ranks[v] = 1f / graph.NVertices;
            newRanks[v] = 1f / graph.NVertices;
        }


        float change = epsilon + 1f;
        while (change > epsilon)
        {

            for (int v = 0; v < graph.NVertices; v++)
                newRanks[v] = PageRank_single(v, graph, ranks, damping);

            // Recalculate change
            change = 0f;
            for (int v = 0; v < graph.NVertices; v++)
                change += MathF.Abs(ranks[v] - newRanks[v]);

            for (int v = 0; v < graph.NVertices; v++)
                ranks[v] = newRanks[v];
        }

        return ranks;
    }

    public static void Main(string[] args)
    {
        string file = args[0];
        string outFile = args[1];

        var graph = new Graph(file);
        var ranks = PageRank(graph, 0.85f);

        using StreamWriter writer = new(outFile);

        for (int v = 0; v < graph.NVertices; v++)
            writer.WriteLine($"{v} {ranks[v]}");
    }
}