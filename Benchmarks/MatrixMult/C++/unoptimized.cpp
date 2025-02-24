#include <cassert>
#include <cstddef>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iomanip>

#define BLOCK_SIZE 8

class Matrix {
public:
  double **values;
  size_t n;

  Matrix(size_t n) {
    this->n = n;

    values = new double *[n];
    for (size_t i = 0; i < n; i++) {
      values[i] = new double[n];
      std::memset(values[i], 0, sizeof(double) * n);
    }
  }

  ~Matrix() {
    for (size_t i = 0; i < n; i++) {
      delete[] values[i];
    }
    delete[] values;
  }
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
    size_t row = index / n;
    size_t col = index % n;
    matrix.values[row][col] = value;
    index++;
  }

  return matrix;
}

static void write(const Matrix &matrix, const char *path) {
  std::ofstream file(path);
  file << std::setprecision(8);
  file << matrix.n << '\n';

  for (size_t i = 0; i < matrix.n; i++) {
    for (size_t j = 0; j < matrix.n; j++) {
      file << matrix.values[i][j] << '\n';
    }
  }

  file.close();
}

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