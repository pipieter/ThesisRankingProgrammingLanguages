
class Fib3 {

    private static long Fibonacci(long value) {
        if (value == 0)
            return 0;
        if (value == 1)
            return 1;
        if (value == 2)
            return 1;

        return Fibonacci(value - 1) + Fibonacci(value - 2) + Fibonacci(value - 3);
    }

    public static void main(String[] args) {

        long value = Long.parseLong(args[0]);
        long result = Fibonacci(value);

        System.out.print(result);

    }
}
