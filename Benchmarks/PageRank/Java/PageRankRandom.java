import java.util.ArrayList;
import java.util.Random;

class GraphRandom {

  public int nvertices;
  public ArrayList<ArrayList<Integer>> incoming;
  public ArrayList<ArrayList<Integer>> outgoing;

  public GraphRandom(int vertices, float density) {
    this.nvertices = vertices;
    this.incoming = new ArrayList<>();
    this.outgoing = new ArrayList<>();

    for (int i = 0; i < vertices; i++) {
      this.incoming.add(new ArrayList<>());
      this.outgoing.add(new ArrayList<>());
    }

    Random random = new Random();
    for (int i = 0; i < vertices; i++) {
      for (int j = 0; j < vertices; j++) {
        float vertex = random.nextFloat();
        if (i != j && vertex < density) {
          this.incoming.get(i).add(j);
          this.outgoing.get(j).add(i);
        }
      }
    }
  }
}

class PageRankRandom {

  public static float PageRank_single(int v, GraphRandom graph, float[] ranks,
                                      float damping) {
    float rank = (1f - damping) / (float)graph.nvertices;
    for (int u : graph.incoming.get(v)) {
      rank += damping * ranks[u] / (float)graph.outgoing.get(u).size();
    }

    return rank;
  }

  public static float[] PageRank(GraphRandom graph, float damping,
                                 float epsilon) {
    float[] ranks = new float[graph.nvertices];
    float[] newRanks = new float[graph.nvertices];

    for (int v = 0; v < graph.nvertices; v++) {
      ranks[v] = 1f / (float)graph.nvertices;
      newRanks[v] = 1f / (float)graph.nvertices;
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

  public static void main(String[] args) {
    int vertices = Integer.parseInt(args[0]);
    float density = Float.parseFloat(args[1]);
    int iterations = Integer.parseInt(args[2]);

    GraphRandom graph = new GraphRandom(vertices, density);
    float totalSum = 0.0f;

    for (int i = 0; i < iterations; i++) {
      float[] ranks = PageRank(graph, 0.85f + (float)i / 1000.0f, 1e-4f);
      for (int r = 0; r < vertices; r++) {
        totalSum += ranks[r];
      }
    }

    System.out.println(totalSum);
  }
}
