#include <fstream>
#include <string>
#include <vector>

using namespace std;

vector<string> merge(const vector<string> &a, const vector<string> &b) {
  vector<string> merged;
  size_t ia = 0;
  size_t ib = 0;

  while (ia < a.size() && ib < b.size()) {
    if (a[ia] < b[ib]) {
      merged.push_back(a[ia]);
      ia++;
    } else {
      merged.push_back(b[ib]);
      ib++;
    }
  }

  for (size_t i = ia; i < a.size(); i++) {
    merged.push_back(a[i]);
  }
  for (size_t i = ib; i < b.size(); i++) {
    merged.push_back(b[i]);
  }

  return merged;
}

vector<string> merge_sort(const vector<string> &entries) {
  if (entries.size() <= 1) {
    return entries;
  }

  int half = entries.size() / 2;
  vector<string> left(entries.begin(), entries.begin() + half);
  vector<string> right(entries.begin() + half, entries.end());

  vector<string> left_sorted = merge_sort(left);
  vector<string> right_sorted = merge_sort(right);

  return merge(left_sorted, right_sorted);
}

int main(int argc, const char **argv) {
  string input = argv[1];
  string output = argv[2];

  string line;
  vector<string> lines;
  ifstream in(input);
  while (getline(in, line)) {
    lines.push_back(line);
  }
  in.close();

  vector<string> sorted = merge_sort(lines);

  ofstream out(output);
  for (const auto &str : sorted) {
    out << str << '\n';
  }
  out.close();

  return 0;
}