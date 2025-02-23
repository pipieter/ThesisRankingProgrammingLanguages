#include <cassert>
#include <cstddef>
#include <cstdlib>
#include <cstring>

#include "matrix.hpp"

Matrix operator*(const Matrix &a, const Matrix &b) {
  assert(a.n == b.n);
  assert(a.n % BLOCK_SIZE == 0);

  size_t n = a.n;
  Matrix matrix(n);

  for (size_t kk = 0; kk < n; kk += BLOCK_SIZE) {
    for (size_t jj = 0; jj < n; jj += BLOCK_SIZE) {
      for (size_t i = 0; i < n; i++) {
        for (size_t j = jj; j < jj + BLOCK_SIZE; j++) {
          for (size_t k = kk; k < kk + BLOCK_SIZE; k++) {
            matrix.values[i][j] += a.values[i][k] * b.values[k][j];
          }
        }
      }
    }
  }

  return matrix;
}

int main(int, const char **argv) {
  Matrix a = read(argv[1]);
  Matrix b = read(argv[2]);
  Matrix c = a * b;

  write(c, argv[3]);

  return 0;
}