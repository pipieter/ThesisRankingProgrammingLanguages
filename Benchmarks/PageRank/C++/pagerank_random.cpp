#include <iostream>
#include <random>
#include <vector>

using namespace std;

class Graph {
public:
  int vertices;
  vector<vector<int>> incoming;
  vector<vector<int>> outgoing;

public:
  Graph(int vertices, float density) {
    this->vertices = vertices;
    this->incoming.resize(vertices);
    this->outgoing.resize(vertices);

    for (int i = 0; i < vertices; i++) {
      for (int j = 0; j < vertices; j++) {
        float vertex = (float)rand() / (float)RAND_MAX;
        if (i != j && vertex < density) {
          incoming[i].push_back(j);
          outgoing[j].push_back(i);
        }
      }
    }
  }
};

float PageRank_single(int v, const Graph &graph, const vector<float> &ranks,
                      float damping) {
  float rank = (1 - damping) / graph.vertices;

  for (int u : graph.incoming[v]) {
    rank += damping * ranks[u] / graph.outgoing[u].size();
  }

  return rank;
}

vector<float> PageRank(const Graph &graph, float damping,
                       float epsilon = 1e-4) {
  vector<float> ranks(graph.vertices);
  vector<float> newRanks(graph.vertices);

  for (int v = 0; v < graph.vertices; v++) {
    ranks[v] = 1.f / graph.vertices;
    newRanks[v] = 1.f / graph.vertices;
  }

  float change = epsilon + 1;
  while (change > epsilon) {
    for (int v = 0; v < graph.vertices; v++) {
      newRanks[v] = PageRank_single(v, graph, ranks, damping);
    }

    change = 0.f;
    for (int v = 0; v < graph.vertices; v++) {
      change += abs(ranks.at(v) - newRanks.at(v));
    }

    for (int v = 0; v < graph.vertices; v++) {
      ranks[v] = newRanks[v];
    }
  }

  return ranks;
}

int main(int argc, const char **argv) {
  int vertices = std::atoi(argv[1]);
  float density = std::atof(argv[2]);
  int iterations = std::atoi(argv[3]);

  Graph graph(vertices, density);
  float total_sum = 0.0f;

  for (int i = 0; i < iterations; i++) {
    auto ranks = PageRank(graph, 0.85f + i / 1000.0);
    for (float r : ranks) {
      total_sum += r;
    }
  }

  std::cout << total_sum << std::endl;

  return 0;
}