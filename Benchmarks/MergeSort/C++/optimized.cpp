#include <cstring>
#include <fstream>
#include <string>
#include <thread>
#include <vector>

using namespace std;

const long int CONCURRENT_THRESHOLD = 10000;

void merge_sort_parallel(const char **start, const char **end);
void merge_sort_concurrent(const char **start, const char **end);

void merge(const char **target, const char **a_start, const char **a_end,
           const char **b_start, const char **b_end) {
  size_t i = 0;

  const char **a = a_start;
  const char **b = b_start;

  while (a != a_end && b != b_end) {
    if (strcmp(*a, *b) < 0) {
      target[i] = *a;
      a++;
    } else {
      target[i] = *b;
      b++;
    }
    i++;
  }

  while (a != a_end) {
    target[i] = *a;
    a++;
    i++;
  }
  while (b != b_end) {
    target[i] = *b;
    b++;
    i++;
  }
}

void merge_sort_parallel(const char **start, const char **end) {
  if ((end - start) <= 1) {
    return;
  }

  if ((end - start) < CONCURRENT_THRESHOLD) {
    merge_sort_concurrent(start, end);
    return;
  }

  size_t half = (end - start) / 2;

  vector<const char *> left(start, start + half);
  vector<const char *> right(start + half, end);

  std::thread left_thread(
      [&left] { merge_sort_parallel(left.data(), left.data() + left.size()); });
  merge_sort_parallel(right.data(), right.data() + right.size());
  left_thread.join();

  merge(start, left.data(), left.data() + left.size(), right.data(),
        right.data() + right.size());
}

void merge_sort_concurrent(const char **start, const char **end) {
  if ((end - start) <= 1) {
    return;
  }

  size_t half = (end - start) / 2;

  vector<const char *> left(start, start + half);
  vector<const char *> right(start + half, end);

  merge_sort_concurrent(left.data(), left.data() + left.size());
  merge_sort_concurrent(right.data(), right.data() + right.size());

  merge(start, left.data(), left.data() + left.size(), right.data(),
        right.data() + right.size());
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

  merge_sort_parallel(lines.data(), lines.data() + lines.size());

  ofstream out(output);
  for (const auto &str : lines) {
    out << str << '\n';
  }
  out.close();

  for (const char *str : lines) {
    delete[] str;
  }

  return 0;
}