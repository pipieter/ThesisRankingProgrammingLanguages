#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

vector<string> splitString(const string &str, char delimiter) {
  stringstream stream(str);
  vector<string> split;
  string current;

  while (getline(stream, current, delimiter)) {
    split.push_back(current);
  }

  return split;
}

class Graph {
public:
  int vertices;
  vector<vector<bool>> incoming;
  vector<int> outgoing;

public:
  Graph(const string &path) {
    vector<vector<bool>> outgoing_edges;
    ifstream file(path);
    string line;

    while (getline(file, line)) {
      if (line[0] == 'p') {
        vector<string> values = splitString(line, ' ');
        int nvertices = atoi(values[2].c_str());

        this->vertices = nvertices;
        this->incoming = vector<vector<bool>>(nvertices);
        this->outgoing = vector<int>(nvertices);
        outgoing_edges = vector<vector<bool>>(nvertices);

        for (int i = 0; i < nvertices; i++) {
          this->incoming[i] = vector<bool>(nvertices);
          outgoing_edges[i] = vector<bool>(nvertices);
        }
      } else if (line[0] == 'a' || line[0] == 'e') {
        vector<string> values = splitString(line, ' ');

        int v0 = atoi(values[1].c_str());
        int v1 = atoi(values[2].c_str());

        outgoing_edges[v0][v1] = true;
        incoming[v1][v0] = true;
      }
    }

    for (int i = 0; i < this->vertices; i++) {
      this->outgoing[i] = std::count(outgoing_edges[i].begin(), outgoing_edges[i].end(), true);
    }

    file.close();
  }
};

float PageRank_single(int v, const Graph &graph, const vector<float> &ranks,
                      float damping) {
  float rank = (1 - damping) / graph.vertices;

  for (int u = 0; u < graph.vertices; u++) {
    if (graph.incoming[v][u]) {
      rank += damping * ranks[u] / graph.outgoing[u];
    }
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
#pragma omp parallel for
    for (int v = 0; v < graph.vertices; v++) {
      newRanks[v] = PageRank_single(v, graph, ranks, damping);
    }

    change = 0.f;
#pragma omp parallel for
    for (int v = 0; v < graph.vertices; v++) {
      change += abs(ranks.at(v) - newRanks.at(v));
    }

    ranks = newRanks;
  }

  return ranks;
}

int main(int, const char **argv) {
  string file = argv[1];
  string out = argv[2];

  Graph graph(file);
  auto ranks = PageRank(graph, 0.85f);

  ofstream outFile(out);

  for (int v = 0; v < graph.vertices; v++) {
    outFile << v << ' ' << ranks[v] << '\n';
  }

  outFile.close();

  return 0;
}