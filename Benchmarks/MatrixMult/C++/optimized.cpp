#include <cassert>
#include <cstddef>
#include <cstdlib>
#include <cstring>
#include <fstream>

#include <cblas.h>
#include <iomanip>

class Matrix {
public:
  double *values;
  size_t n;

  Matrix(size_t n) {
    this->n = n;

    values = new double[n * n];
    std::memset(values, 0, sizeof(double) * n * n);
  }

  ~Matrix() { delete[] values; }
};

static Matrix read(const char *path) {
  std::ifstream file(path);
  std::string line;

  std::getline(file, line);
  size_t n = std::atoi(line.c_str());

  Matrix matrix(n);

  size_t index = 0;
  while (std::getline(file, line)) {
    double value = std::atof(line.c_str());
    matrix.values[index] = value;
    index++;
  }

  return matrix;
}

static void write(const Matrix &matrix, const char *path) {
  std::ofstream file(path);
  file << std::setprecision(8);
  file << matrix.n << '\n';

  for (size_t i = 0; i < matrix.n * matrix.n; i++) {
    file << matrix.values[i] << '\n';
  }

  file.close();
}

Matrix operator*(const Matrix &a, const Matrix &b) {
  assert(a.n == b.n);

  size_t n = a.n;
  Matrix c = Matrix(n);

  cblas_dgemm(CblasColMajor, CblasNoTrans, CblasNoTrans, n, n, n, 1.0, a.values,
              n, b.values, n, 1.0, c.values, n);

  return c;
}

int main(int, const char **argv) {
  Matrix a = read(argv[1]);
  Matrix b = read(argv[2]);
  Matrix c = a * b;

  write(c, argv[3]);

  return 0;
}