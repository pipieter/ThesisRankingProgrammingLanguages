#include <cassert>
#include <cstddef>
#include <cstdlib>
#include <cstring>

#include "matrix.hpp"

void matrixmultiply(double **__restrict a, double **__restrict b,
                    double **__restrict c, size_t n) {
  assert(n % BLOCK_SIZE == 0);

  for (size_t kk = 0; kk < n; kk += BLOCK_SIZE) {
    for (size_t jj = 0; jj < n; jj += BLOCK_SIZE) {
      for (size_t i = 0; i < n; i++) {
        for (size_t j = jj; j < jj + BLOCK_SIZE; j++) {
          for (size_t k = kk; k < kk + BLOCK_SIZE; k++) {
            c[i][j] += a[i][k] * b[k][j];
          }
        }
      }
    }
  }
}

int main(int, const char **argv) {
  Matrix a = read(argv[1]);
  Matrix b = read(argv[2]);
  Matrix c = Matrix(a.n);

  matrixmultiply(a.values, b.values, c.values, a.n);

  write(c, argv[3]);

  return 0;
}