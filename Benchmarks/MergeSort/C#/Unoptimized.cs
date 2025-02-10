namespace MergeSort.Unoptimized;


public class MergeSorter
{
    public static List<string> Sort(List<string> entries)
    {
        if (entries.Count <= 1)
        {
            return entries;
        }

        int half = entries.Count / 2;
        List<string> left = Sort(entries[0..half]);
        List<string> right = Sort(entries[half..entries.Count]);

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
        string input = args[0];
        string output = args[1];

        List<string> lines = [.. File.ReadAllLines(input)];
        List<string> sorted = Sort(lines);

        File.WriteAllLines(output, sorted);
    }
}
