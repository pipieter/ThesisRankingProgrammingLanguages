using System.Linq;

class Graph
{
    public System.Collections.Generic.List<int>[] Outgoing;
    public System.Collections.Generic.List<int>[] Incoming;
    public int NVertices = 0;

    public Graph(string path)
    {
        System.Collections.Generic.List<System.Collections.Generic.HashSet<int>> incoming = new System.Collections.Generic.List<System.Collections.Generic.HashSet<int>>();
        System.Collections.Generic.List<System.Collections.Generic.HashSet<int>> outgoing = new System.Collections.Generic.List<System.Collections.Generic.HashSet<int>>();

        using (System.IO.StreamReader reader = new System.IO.StreamReader(path))
        {
            string line = reader.ReadLine();
            while (line != null)
            {
                if (line.StartsWith('p'))
                {
                    string[] values = line.Split(' ');
                    int vertices = int.Parse(values[2]);

                    NVertices = vertices;
                    outgoing.Clear();
                    incoming.Clear();
                    for (int i = 0; i < vertices; i++)
                    {
                        outgoing.Add(new System.Collections.Generic.HashSet<int>());
                        incoming.Add(new System.Collections.Generic.HashSet<int>());
                    }
                }
                else if (line.StartsWith('a') || line.StartsWith('e'))
                {
                    string[] values = line.Split(' ');
                    int a = int.Parse(values[1]);
                    int b = int.Parse(values[2]);

                    outgoing[a].Add(b);
                    incoming[b].Add(a);
                }

                line = reader.ReadLine();
            }
        }

        // Remove duplicates
        Outgoing = new System.Collections.Generic.List<int>[NVertices];
        Incoming = new System.Collections.Generic.List<int>[NVertices];
        for (int i = 0; i < NVertices; i++)
        {
            Outgoing[i] = outgoing[i].ToList();
            Incoming[i] = incoming[i].ToList();
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
                change += System.MathF.Abs(ranks[v] - newRanks[v]);

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

        using (System.IO.StreamWriter writer = new System.IO.StreamWriter(outFile))
        {
            for (int v = 0; v < graph.NVertices; v++)
                writer.WriteLine($"{v} {ranks[v]}");
        }
    }
}