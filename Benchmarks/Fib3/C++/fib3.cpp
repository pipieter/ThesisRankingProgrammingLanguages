#include <cstdint>
#include <iostream>

using namespace std;

int64_t fib3(int64_t value) {
  if (value == 0)
    return 0;
  if (value == 1)
    return 1;
  if (value == 2)
    return 1;

  return fib3(value - 1) + fib3(value - 2) + fib3(value - 3);
}

int main(int argc, const char **argv) {
  int64_t value = atol(argv[1]);
  int64_t result = fib3(value);

  std::cout << result << std::endl;

  return 0;
}