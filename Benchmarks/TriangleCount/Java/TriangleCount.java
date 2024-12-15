
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;

class Graph {

    public int nvertices;
    public ArrayList<HashSet<Integer>> edges;

    public Graph(String file) throws FileNotFoundException, IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {

            String line = reader.readLine();

            while (line != null) {
                if (line.startsWith("p")) {
                    String[] values = line.split(" ");
                    int vertices = Integer.parseInt(values[2]);

                    this.nvertices = vertices;
                    this.edges = new ArrayList<>(vertices);
                    for (int i = 0; i < vertices; i++) {
                        this.edges.add(new HashSet<>());
                    }
                } else if (line.startsWith("e") || line.startsWith("a")) {
                    String[] values = line.split(" ");

                    int a = Integer.parseInt(values[1]);
                    int b = Integer.parseInt(values[2]);

                    if (a != b) {
                        this.edges.get(a).add(b);
                        this.edges.get(b).add(a);
                    }
                }

                line = reader.readLine();
            }
        }
    }
}

class TriangleCount {

    public static int TriangleCount_single(Graph graph, int a, int b) {
        if (a >= b)
            return 0;

        HashSet<Integer> edgesA = graph.edges.get(a);
        HashSet<Integer> edgesB = graph.edges.get(b);

        HashSet<Integer> intersection = new HashSet<>(edgesA);
        intersection.retainAll(edgesB);

        return intersection.size();

    }

    public static int Count(Graph graph) {
        int count = 0;

        for (int a = 0; a < graph.nvertices; a++) {
            for (int b = a + 1; b < graph.nvertices; b++) {
                count += TriangleCount_single(graph, a, b);
            }
        }

        return count;
    }

    public static void main(String[] args) throws FileNotFoundException, IOException {
        String file = args[0];

        Graph graph = new Graph(file);
        int count = Count(graph);

        System.out.println(count);
    }
}
