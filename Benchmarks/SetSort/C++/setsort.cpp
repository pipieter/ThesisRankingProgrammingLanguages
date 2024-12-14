#include <fstream>
#include <set>
#include <string>

using namespace std;

void set_sort(const string &in, const string &out) {
  set<int> values;

  // Read file
  {
    ifstream file(in);
    string line;

    while (getline(file, line)) {
      int value = atoi(line.c_str());
      values.insert(value);
    }
  }

  // Write file
  {
    ofstream file(out);

    for (int value : values) {
      file << value << '\n';
    }
  }
}

int main(int argc, const char **argv) {
  string in = argv[1];
  string out = argv[2];

  set_sort(in, out);
}