public class Fibonacci
{
    private static long Fib3(long value)
    {
        if (value == 0) return 0;
        if (value == 1) return 1;
        if (value == 2) return 1;

        return Fib3(value - 1) + Fib3(value - 2) + Fib3(value - 3);
    }

    public static void Main(string[] args)
    {
        long value = long.Parse(args[0]);
        long result = Fibonacci.Fib3(value);

        System.Console.WriteLine(result);
    }
}
