#pragma once

#include <cstddef>
#include <cstring>
#include <fstream>

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
  file << matrix.n << '\n';

  for (size_t i = 0; i < matrix.n; i++) {
    for (size_t j = 0; j < matrix.n; j++) {
      file << matrix.values[i][j] << '\n';
    }
  }

  file.close();
}