class GraphRandom
{
    public System.Collections.Generic.List<int>[] Outgoing;
    public System.Collections.Generic.List<int>[] Incoming;
    public int NVertices = 0;

    public GraphRandom(int vertices, float density)
    {
        NVertices = vertices;
        Outgoing = new System.Collections.Generic.List<int>[vertices];
        Incoming = new System.Collections.Generic.List<int>[vertices];

        for (int i = 0; i < vertices; i++)
        {
            Outgoing[i] = new System.Collections.Generic.List<int>();
            Incoming[i] = new System.Collections.Generic.List<int>();
        }

        System.Random random = new System.Random();
        for (int i = 0; i < vertices; i++)
        {
            for (int j = 0; j < vertices; j++)
            {
                float vertex = (float)random.NextDouble();
                if (i != j && vertex < density)
                {
                    Outgoing[i].Add(j);
                    Incoming[j].Add(i);
                }
            }
        }
    }
}

class PageRankRandom
{
    public static float PageRank_single(int v, GraphRandom graph, float[] ranks, float damping)
    {
        float rank = (1.0f - damping) / graph.NVertices;

        foreach (int u in graph.Incoming[v])
            rank += damping * ranks[u] / graph.Outgoing[u].Count;

        return rank;
    }

    public static float[] PageRank(GraphRandom graph, float damping, float epsilon = 1e-4f)
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
                change += System.MathF.Abs(ranks[v] - newRanks[v]);

            for (int v = 0; v < graph.NVertices; v++)
                ranks[v] = newRanks[v];
        }

        return ranks;
    }

    public static void Main(string[] args)
    {
        int vertices = int.Parse(args[0]);
        float density = float.Parse(args[1]);
        int iterations = int.Parse(args[2]);

        var graph = new GraphRandom(vertices, density);

        float totalSum = 0.0f;

        for (int i = 0; i < iterations; i++)
        {
            var ranks = PageRank(graph, 0.85f + i / 1000.0f); 
            for (int r = 0; r < vertices; r++)
            {
                totalSum += ranks[r];
            }
        }

        System.Console.WriteLine(totalSum);
    }
}