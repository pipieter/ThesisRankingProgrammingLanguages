import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class Matrix {
    static final int BLOCK_SIZE = 8;
    public double[][] values;
    public int n;

    public Matrix(int n) {
        this.n = n;
        this.values = new double[n][n];
    }

    public static Matrix Read(String path) throws FileNotFoundException, IOException, NumberFormatException {
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            int n = Integer.parseInt(reader.readLine());
            Matrix matrix = new Matrix(n);

            int index = 0;
            while (true) {
                String line = reader.readLine();
                if (line == null) {
                    break;
                }
                int row = index / n;
                int col = index % n;
                double value = Double.parseDouble(line);
                matrix.values[row][col] = value;

                index += 1;
            }
            return matrix;
        }

    }

    public static void Write(Matrix matrix, String path) throws IOException {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(path))) {
            writer.write(Integer.toString(matrix.n));
            writer.newLine();

            for (int i = 0; i < matrix.n; i++) {
                for (int j = 0; j < matrix.n; j++) {
                    writer.write((Double.toString(matrix.values[i][j])));
                    writer.newLine();
                }
            }
        }
    }

    public static Matrix Multiply(Matrix a, Matrix b) {
        assert (a.n == b.n);
        assert (a.n % BLOCK_SIZE == 0);

        int n = a.n;
        Matrix matrix = new Matrix(n);

        for (int kk = 0; kk < n; kk += BLOCK_SIZE) {
            for (int jj = 0; jj < n; jj += BLOCK_SIZE) {
                for (int i = 0; i < n; i++) {
                    for (int j = jj; j < jj + BLOCK_SIZE; j++) {
                        for (int k = kk; k < kk + BLOCK_SIZE; k++) {
                            matrix.values[i][j] += a.values[i][k] * b.values[k][j];
                        }
                    }
                }

            }
        }

        return matrix;
    }

    public static void main(String[] args) throws NumberFormatException, FileNotFoundException, IOException {
        Matrix a = Read(args[0]);
        Matrix b = Read(args[1]);
        Matrix c = Multiply(a, b);

        Write(c, args[2]);
    }
}