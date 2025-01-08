using System.IO;

namespace MergeSort;


public class MergeSorter
{
    public static List<string> MergeSort(List<string> entries)
    {
        if (entries.Count <= 1)
        {
            return entries;
        }

        int half = entries.Count / 2;
        List<string> left = MergeSort(entries[0..half]);
        List<string> right = MergeSort(entries[half..entries.Count]);

        return Merge(left, right);
    }

    public static List<string> Merge(List<string> a, List<string> b)
    {
        List<string> merged = [];
        int ia = 0;
        int ib = 0;

        while (ia < a.Count && ib < b.Count)
        {
            if (string.CompareOrdinal(a[ia], b[ib]) < 0)
            {
                merged.Add(a[ia]);
                ia += 1;
            }
            else
            {
                merged.Add(b[ib]);
                ib += 1;
            }
        }

        merged.AddRange(a[ia..a.Count]);
        merged.AddRange(b[ib..b.Count]);

        return merged;
    }


    public static void Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.Error.WriteLine("Usage: program [input] [output]");
            return;
        }

        string input = args[0];
        string output = args[1];

        List<string> lines = [.. File.ReadAllLines(input)];
        List<string> sorted = MergeSort(lines);

        File.WriteAllLines(output, sorted);
    }
}
