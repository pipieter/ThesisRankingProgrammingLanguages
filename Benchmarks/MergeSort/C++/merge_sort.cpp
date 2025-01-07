#include <algorithm>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

vector<vector<string>> split_blocks(const string &path, int blockSize) {
  vector<vector<string>> blocks;
  vector<string> lines;

  ifstream file(path);
  int bytesRead = 0;

  while (true) {
    string line;
    if (!getline(file, line)) {
      break;
    }

    lines.push_back(line);
    bytesRead += line.size();

    if (bytesRead >= blockSize) {
      sort(lines.begin(), lines.end(), greater<>());

      blocks.push_back(lines);
      lines.clear();
      bytesRead = 0;
    }
  }

  if (lines.size() > 0) {
    sort(lines.begin(), lines.end(), greater<>());
    blocks.push_back(lines);
  }

  return blocks;
}

vector<string> merge_blocks(vector<vector<string>> blocks) {
  vector<string> sorted;

  while (true) {
    int block = -1;

    for (int i = 0; i < blocks.size(); i++) {
      if (blocks[i].empty()) {
        continue;
      }

      if (block == -1) {
        block = i;
      } else {
        string current = blocks[block].back();
        string next = blocks[i].back();

        if (next < current) {
          block = i;
        }
      }
    }

    if (block == -1) {
      break;
    }

    string value = blocks[block].back();
    sorted.push_back(value);
    blocks[block].pop_back();
  }

  return sorted;
}

int main(int argc, const char **argv) {
  string file = argv[1];
  string outFile = argv[2];
  int blockSize = atoi(argv[3]);

  auto blocks = split_blocks(file, blockSize);
  auto sorted = merge_blocks(blocks);

  ofstream out(outFile);
  for (const auto &str : sorted) {
    out << str << '\n';
  }
  out.close();

  return 0;
}