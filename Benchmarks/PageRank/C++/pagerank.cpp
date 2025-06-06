#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_set>
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
  vector<vector<int>> incoming;
  vector<vector<int>> outgoing;

public:
  Graph(const string &path) {
    ifstream file(path);
    string line;

    vector<unordered_set<int>> incoming_sets;
    vector<unordered_set<int>> outgoing_sets;

    while (getline(file, line)) {
      if (line[0] == 'p') {
        vector<string> values = splitString(line, ' ');
        int nvertices = atoi(values[2].c_str());

        this->vertices = nvertices;
        incoming_sets.clear();
        outgoing_sets.clear();
        incoming_sets.resize(nvertices);
        outgoing_sets.resize(nvertices);
      } else if (line[0] == 'a' || line[0] == 'e') {
        vector<string> values = splitString(line, ' ');

        int v0 = atoi(values[1].c_str());
        int v1 = atoi(values[2].c_str());

        outgoing_sets[v0].insert(v1);
        incoming_sets[v1].insert(v0);
      }
    }

    file.close();

    // Remove duplicates
    incoming.resize(vertices);
    outgoing.resize(vertices);
    for (int v = 0; v < vertices; v++) {
      outgoing[v].assign(outgoing_sets[v].begin(), outgoing_sets[v].end());
      incoming[v].assign(incoming_sets[v].begin(), incoming_sets[v].end());
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