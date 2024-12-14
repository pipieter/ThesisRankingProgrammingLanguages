#include <algorithm>
#include <fstream>
#include <string>
#include <unordered_set>
#include <vector>

using namespace std;

void set_sort(const string &in, const string &out) {
  unordered_set<int> set;

  // Read file
  {
    ifstream file(in);
    string line;

    while (getline(file, line)) {
      int value = atoi(line.c_str());
      set.insert(value);
    }
  }

  // Write file
  {
    ofstream file(out);
    vector<int> vec(set.begin(), set.end());
    sort(vec.begin(), vec.end());

    for (int value : vec) {
      file << value << '\n';
    }
  }
}

int main(int argc, const char **argv) {
  string in = argv[1];
  string out = argv[2];

  set_sort(in, out);
}