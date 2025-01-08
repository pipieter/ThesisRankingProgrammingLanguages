#include <cstring>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

vector<const char *> merge(const char **a_start, const char **a_end,
                           const char **b_start, const char **b_end) {
  size_t size = (a_end - a_start) + (b_end - b_start);
  vector<const char *> merged(size);
  size_t i = 0;

  const char **a = a_start;
  const char **b = b_start;

  while (a != a_end && b != b_end) {
    if (strcmp(*a, *b) < 0) {
      merged[i] = *a;
      a++;
    } else {
      merged[i] = *b;
      b++;
    }
    i++;
  }

  while (a != a_end) {
    merged[i] = *a;
    a++;
    i++;
  }
  while (b != b_end) {
    merged[i] = *b;
    b++;
    i++;
  }

  return merged;
}

vector<const char *> merge_sort(const char **start, const char **end) {
  if ((end - start) <= 1) {
    return vector<const char *>(start, end);
  }

  size_t half = (end - start) / 2;
  size_t diff = end - start;

  vector<const char *> left_sorted = merge_sort(start, start + half);
  vector<const char *> right_sorted = merge_sort(start + half, end);

  return merge(left_sorted.data(), left_sorted.data() + left_sorted.size(),
               right_sorted.data(), right_sorted.data() + right_sorted.size());
}

int main(int argc, const char **argv) {
  string input = argv[1];
  string output = argv[2];

  string line;
  vector<const char *> lines;
  ifstream in(input);
  while (getline(in, line)) {
    char *str = new char[line.size() + 1];
    strncpy(str, line.data(), line.size());
    str[line.size()] = '\0';
    lines.push_back(str);
  }
  in.close();

  vector<const char *> sorted =
      merge_sort(lines.data(), lines.data() + lines.size());

  ofstream out(output);
  for (const auto &str : sorted) {
    out << str << '\n';
  }
  out.close();

  for (const char *str : lines) {
    delete[] str;
  }

  return 0;
}