// g++ optimized_zero.cpp -o ./optimized_zero -O3 -march=native -lopenblas

#include <cblas.h>
#include <iostream>

int main(int, const char **argv) {
  size_t size = std::atoll(argv[1]);
  double *a = (double *)calloc(size * size, sizeof(double));
  double *b = (double *)calloc(size * size, sizeof(double));
  double *c = (double *)calloc(size * size, sizeof(double));

  cblas_dgemm(CblasColMajor, CblasNoTrans, CblasNoTrans, size, size, size, 1.0,
              a, size, b, size, 1.0, c, size);

  std::cout << c[0] << std::endl;

  return 0;
}

