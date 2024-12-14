#include <cstdio>
#include <exception>
#include <fstream>
#include <sstream>
#include <string>

using namespace std;

int read_file(const string &path) {
  try {
    ifstream file(path);
    stringstream buffer;
    buffer << file.rdbuf();
    return atoi(buffer.str().c_str());
  } catch (exception &) {
    return 0;
  }
}

void write_file(const string &path, int value) {
  ofstream file(path);
  file << value;
}

void run(int count, const string &path) {
  remove(path.c_str());
  int value = 0;
  while (value != count) {
    value = read_file(path);
    write_file(path, value + 1);
  }
}

int main(int argc, const char **argv) {
  int count = atoi(argv[1]);
  string path = argv[2];

  run(count, path);
}