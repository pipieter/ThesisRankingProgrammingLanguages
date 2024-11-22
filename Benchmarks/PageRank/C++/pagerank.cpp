#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>

using namespace std;

class Graph {
public:
  int vertices;
  vector<unordered_set<int>> incoming;
  vector<unordered_set<int>> outgoing;

public:
  Graph(const string &path) {
    ifstream file(path);

    string line;
    getline(file, line);

    int nvertices = atoi(line.c_str());
    this->vertices = nvertices;
    this->incoming = vector<unordered_set<int>>(nvertices);
    this->outgoing = vector<unordered_set<int>>(nvertices);

    while (getline(file, line)) {
      size_t splitpos = line.find(" ");
      string str_a = line.substr(0, splitpos);
      string str_b = line.substr(splitpos + 1, line.length());

      int a = atoi(str_a.c_str());
      int b = atoi(str_b.c_str());

      outgoing[a].insert(b);
      incoming[b].insert(a);
    }

    file.close();
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
  string file = argv[1];
  string out = argv[2];

  Graph graph(file);
  auto ranks = PageRank(graph, 0.85f);

  ofstream outFile(out);

  for (int v = 0; v < graph.vertices; v++) {
    outFile << v << ' ' << ranks[v] << '\n';
  }

  outFile.close();
}