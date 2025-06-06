
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;

class Graph {

    public int nvertices;
    public ArrayList<ArrayList<Integer>> incoming;
    public ArrayList<ArrayList<Integer>> outgoing;

    public Graph(String file) throws FileNotFoundException, IOException {
        ArrayList<HashSet<Integer>> incomingSets = new ArrayList<>();
        ArrayList<HashSet<Integer>> outgoingSets = new ArrayList<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {

            String line = reader.readLine();

            while (line != null) {
                if (line.startsWith("p")) {
                    String[] values = line.split(" ");
                    int vertices = Integer.parseInt(values[2]);

                    this.nvertices = vertices;
                    incomingSets.clear();
                    outgoingSets.clear();
                    incomingSets.ensureCapacity(vertices);
                    outgoingSets.ensureCapacity(vertices);
                    for (int i = 0; i < vertices; i++) {
                        incomingSets.add(new HashSet<>());
                        outgoingSets.add(new HashSet<>());
                    }
                } else if (line.startsWith("e") || line.startsWith("a")) {
                    String[] values = line.split(" ");

                    int a = Integer.parseInt(values[1]);
                    int b = Integer.parseInt(values[2]);

                    outgoingSets.get(a).add(b);
                    incomingSets.get(b).add(a);
                }

                line = reader.readLine();
            }
        }

        // Remove duplicates
        this.incoming = new ArrayList<>(this.nvertices);
        this.outgoing = new ArrayList<>(this.nvertices);
        for (int i = 0; i < this.nvertices; i++) {
            this.outgoing.add(new ArrayList<>(outgoingSets.get(i)));
            this.incoming.add(new ArrayList<>(incomingSets.get(i)));
        }

    }
}

class PageRank {

    public static float PageRank_single(int v, Graph graph, float[] ranks, float damping) {
        float rank = (1f - damping) / (float) graph.nvertices;
        for (int u : graph.incoming.get(v)) {
            rank += damping * ranks[u] / (float) graph.outgoing.get(u).size();
        }

        return rank;
    }

    public static float[] PageRank(Graph graph, float damping, float epsilon) {
        float[] ranks = new float[graph.nvertices];
        float[] newRanks = new float[graph.nvertices];

        for (int v = 0; v < graph.nvertices; v++) {
            ranks[v] = 1f / (float) graph.nvertices;
            newRanks[v] = 1f / (float) graph.nvertices;
        }

        float change = epsilon + 1f;
        while (change > epsilon) {
            for (int v = 0; v < graph.nvertices; v++) {
                newRanks[v] = PageRank_single(v, graph, ranks, damping);
            }

            change = 0f;
            for (int v = 0; v < graph.nvertices; v++) {
                change += Math.abs(ranks[v] - newRanks[v]);
            }

            for (int v = 0; v < graph.nvertices; v++) {
                ranks[v] = newRanks[v];
            }
        }

        return ranks;
    }

    public static void main(String[] args) throws FileNotFoundException, IOException {
        String file = args[0];
        String out = args[1];

        Graph graph = new Graph(file);
        float[] ranks = PageRank(graph, 0.85f, 1e-4f);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(out))) {
            for (int i = 0; i < ranks.length; i++) {
                String line = String.format("%d %f\n", i, ranks[i]);
                writer.write(line);

            }
        }
    }
}
