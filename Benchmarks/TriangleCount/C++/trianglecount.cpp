#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <iterator>
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
  vector<unordered_set<int>> edges;

public:
  Graph(const string &path) {
    ifstream file(path);
    string line;

    while (getline(file, line)) {
      if (line[0] == 'p') {
        vector<string> values = splitString(line, ' ');
        int nvertices = atoi(values[2].c_str());

        this->vertices = nvertices;
        this->edges = vector<unordered_set<int>>(nvertices);
      } else if (line[0] == 'a' || line[0] == 'e') {
        vector<string> values = splitString(line, ' ');

        int v0 = atoi(values[1].c_str());
        int v1 = atoi(values[2].c_str());

        if (v0 != v1) {
          edges[v0].insert(v1);
          edges[v1].insert(v0);
        }
      }
    }

    file.close();
  }
};

int TriangleCount_single(const Graph &graph, int a, int b) {
  if (a >= b)
    return 0;

  auto edgesA = graph.edges[a];
  auto edgesB = graph.edges[b];

  vector<int> intersection;
  set_intersection(edgesA.begin(), edgesA.end(), edgesB.begin(), edgesB.end(),
                   back_inserter(intersection));

  return intersection.size();
}

int TriangleCount(const Graph &graph) {
  int count = 0;

  for (int a = 0; a < graph.vertices; a++) {
    for (int b = a + 1; b < graph.vertices; b++) {
      count += TriangleCount_single(graph, a, b);
    }
  }

  return count;
}

int main(int argc, const char **argv) {
  string file = argv[1];

  Graph graph(file);
  auto count = TriangleCount(graph);

  std::cout << count << std::endl;

  return 0;
}