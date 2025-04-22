using System.Runtime.InteropServices;

namespace Optimized;

public class MatrixMult
{
    [DllImport("libopenblas.so", EntryPoint = "cblas_dgemm")]
    static extern unsafe void cblas_dgemm(int Order, int TransA, int TransB, int M, int N, int K, double alpha, double* A, int lda, double* B, int ldb, double beta, double* C, int ldc);

    const int CblasColMajor = 102;
    const int CblasNoTrans = 111;

    public unsafe static void Main(string[] args)
    {
        int size = int.Parse(args[0]);
        double[] aArray = new double[size * size];
        double[] bArray = new double[size * size];
        double[] cArray = new double[size * size];

        fixed (double* a = aArray, b = bArray, c = cArray)
        {
            cblas_dgemm(CblasColMajor, CblasNoTrans, CblasNoTrans, size, size, size, 1.0, a, size, b, size, 1.0, c, size);
        }

        Console.WriteLine(cArray[0]);
    }

}