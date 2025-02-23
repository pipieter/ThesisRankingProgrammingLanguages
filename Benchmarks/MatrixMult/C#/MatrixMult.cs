public class Matrix
{
    const int BLOCK_SIZE = 8;

    public double[,] values;
    public readonly int n;

    public Matrix(int n)
    {
        this.n = n;
        this.values = new double[n, n];
    }

    public static Matrix Read(string path)
    {
        using (System.IO.StreamReader reader = new System.IO.StreamReader(path))
        {
            string line = reader.ReadLine();
            int n = int.Parse(line);

            Matrix matrix = new Matrix(n);

            int index = 0;
            while (true)
            {
                line = reader.ReadLine();
                if (line == null)
                {
                    break;
                }
                int row = index / n;
                int col = index % n;

                matrix.values[row, col] = double.Parse(line);
                index += 1;
            }
            return matrix;
        }
    }

    public static void Write(Matrix matrix, string path)
    {
        using (System.IO.StreamWriter writer = new System.IO.StreamWriter(path))
        {
            writer.WriteLine(matrix.n.ToString());

            for (int i = 0; i < matrix.n; i++)
                for (int j = 0; j < matrix.n; j++)
                    writer.WriteLine(matrix.values[i, j].ToString());

        }
    }

    public static Matrix Multiply(Matrix a, Matrix b)
    {
        System.Diagnostics.Debug.Assert(a.n == b.n);
        System.Diagnostics.Debug.Assert(a.n % BLOCK_SIZE == 0);

        int n = a.n;
        Matrix matrix = new Matrix(n);

        for (int kk = 0; kk < n; kk += BLOCK_SIZE)
            for (int jj = 0; jj < n; jj += BLOCK_SIZE)
                for (int i = 0; i < n; i++)
                    for (int j = jj; j < jj + BLOCK_SIZE; j++)
                        for (int k = kk; k < kk + BLOCK_SIZE; k++)
                            matrix.values[i, j] += a.values[i, k] * b.values[k, j];

        return matrix;
    }

    public static void Main(string[] args) {
        Matrix a = Read(args[0]);
        Matrix b = Read(args[1]);
        Matrix c = Multiply(a, b);

        Write(c, args[2]);
    }
}