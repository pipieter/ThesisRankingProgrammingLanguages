namespace MergeSort.Unoptimized;


public class MergeSorter
{
    const int ConcurrentThreshold = 10_000;

    public static void SortConcurrent(string[] entries)
    {
        if (entries.Length <= 1)
            return;

        int half = entries.Length / 2;
        string[] left = [.. entries.Take(half)];
        string[] right = [.. entries.Skip(half)];

        SortConcurrent(left);
        SortConcurrent(right);

        Merge(left, right, entries);
    }

    public static void SortParallel(string[] entries)
    {
        if (entries.Length < ConcurrentThreshold)
        {
            SortConcurrent(entries);
            return;
        }


        int half = entries.Length / 2;
        string[] left = [.. entries.Take(half)];
        string[] right = [.. entries.Skip(half)];

        Thread leftThread = new(() => { SortParallel(left); });
        leftThread.Start();

        SortParallel(right);
        leftThread.Join();

        Merge(left, right, entries);
    }

    public static void Merge(string[] a, string[] b, string[] target)
    {
        int i = 0;
        int ia = 0;
        int ib = 0;

        while (ia < a.Length && ib < b.Length)
        {
            if (string.CompareOrdinal(a[ia], b[ib]) < 0)
            {
                target[i] = a[ia];
                ia += 1;
            }
            else
            {
                target[i] = b[ib];
                ib += 1;
            }
            i += 1;
        }

        Array.Copy(a, ia, target, i, a.Length - ia);
        i += a.Length - ia;
        Array.Copy(b, ib, target, i, b.Length - ib);
    }


    public static void Main(string[] args)
    {
        string input = args[0];
        string output = args[1];

        string[] lines = [.. File.ReadAllLines(input)];
        SortParallel(lines);

        File.WriteAllLines(output, lines);
    }
}
