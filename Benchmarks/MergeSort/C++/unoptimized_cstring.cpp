#include <cstring>
#include <fstream>
#include <string>
#include <vector>

// This is the same implementation as unoptimized.cpp, except C-strings are used instead of std::strings.
// A speed-up of about x3.454 was noted

using namespace std;

vector<const char *> merge(const vector<const char *> &a,
                           const vector<const char *> &b) {
  vector<const char *> merged;
  size_t ia = 0;
  size_t ib = 0;

  while (ia < a.size() && ib < b.size()) {
    if (std::strcmp(a[ia], b[ib]) < 0) {
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

vector<const char *> merge_sort(const vector<const char *> &entries) {
  if (entries.size() <= 1) {
    return entries;
  }

  int half = entries.size() / 2;
  vector<const char *> left(entries.begin(), entries.begin() + half);
  vector<const char *> right(entries.begin() + half, entries.end());

  vector<const char *> left_sorted = merge_sort(left);
  vector<const char *> right_sorted = merge_sort(right);

  return merge(left_sorted, right_sorted);
}

int main(int argc, const char **argv) {
  string input = argv[1];
  string output = argv[2];

  string line;
  vector<const char *> lines;
  ifstream in(input);
  while (getline(in, line)) {
    char *cstring = new char[line.size() + 1];
    strcpy(cstring, line.c_str());
    cstring[line.size()] = '\0';
    lines.push_back(cstring);
  }
  in.close();

  vector<const char *> sorted = merge_sort(lines);

  ofstream out(output);
  for (const auto &str : sorted) {
    out << str << '\n';
  }
  out.close();

  for (auto line : lines) {
    delete line;
  }

  return 0;
}