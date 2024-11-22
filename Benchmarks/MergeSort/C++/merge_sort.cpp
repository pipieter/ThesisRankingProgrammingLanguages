#include <algorithm>
#include <deque>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

class Block {
private:
  ifstream file;
  deque<string> values;
  int blockSize;
  bool fileHasRemaining;

public:
  Block(const string &path, int blockSize) {
    this->file = ifstream(path);
    this->blockSize = blockSize;
    this->fileHasRemaining = true;
  }

  string next() {
    if (this->values.empty() && this->fileHasRemaining) {
      this->readNext();
    }

    if (this->values.empty()) {
      return "";
    }

    return this->values.front();
  }

  void pop() { this->values.pop_front(); }

private:
  void readNext() {
    if (!this->fileHasRemaining)
      return;

    this->values.clear();

    int bytesRead = 0;
    while (bytesRead < this->blockSize) {
      string line;
      if (!getline(this->file, line)) {
        this->fileHasRemaining = false;
        return;
      }

      this->values.push_back(line);
      bytesRead += line.size();
    }
  }
};

string write_block(const vector<string> &lines, int index) {
  string fileName = string("temp/block.") + to_string(index) + string(".temp");
  ofstream out(fileName);

  for (const string &line : lines) {
    out << line << '\n';
  }

  out.close();
  return fileName;
}

vector<string> split_blocks(const string &path, int blockSize) {
  vector<string> files;
  vector<string> lines;

  ifstream file(path);
  int bytesRead = 0;
  int index = 0;

  while (true) {
    string line;
    if (!getline(file, line)) {
      break;
    }

    lines.push_back(line);
    bytesRead += line.size();

    if (bytesRead >= blockSize) {
      sort(lines.begin(), lines.end());
      string fileName = write_block(lines, index);

      files.push_back(fileName);
      lines.clear();
      bytesRead = 0;
      index++;
    }
  }

  if (lines.size() > 0) {
    sort(lines.begin(), lines.end());
    string fileName = write_block(lines, index);
    files.push_back(fileName);
  }

  return files;
}

void merge_blocks(const vector<string> &files, string out, int blockSize) {
  vector<Block> blocks;
  for (const string &file : files) {
    blocks.push_back(Block(file, blockSize));
  }

  ofstream outFile(out);

  while (true) {
    int block = -1;
    string value = "";

    for (int i = 0; i < blocks.size(); i++) {
      string blockValue = blocks[i].next();
      if (blockValue.empty()) {
        continue;
      }

      if (value.empty() || blockValue < value) {
        block = i;
        value = blockValue;
      }
    }

    if (block == -1) {
      break;
    }

    blocks[block].pop();
    outFile << value << '\n';
  }

  outFile.close();
}

int main(int argc, const char **argv) {
  string file = argv[1];
  string out = argv[2];
  int blockSize = atoi(argv[3]);

  auto files = split_blocks(file, blockSize);
  merge_blocks(files, out, blockSize / files.size());

  return 0;
}