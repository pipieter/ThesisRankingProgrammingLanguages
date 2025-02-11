using System.Linq;

public class MergeSorter
{
    public static System.Collections.Generic.List<string> Sort(System.Collections.Generic.List<string> entries)
    {
        if (entries.Count <= 1)
        {
            return entries;
        }

        int half = entries.Count / 2;
        System.Collections.Generic.List<string> left = Sort(entries.Take(half).ToList<string>());
        System.Collections.Generic.List<string> right = Sort(entries.Skip(half).Take(entries.Count - half).ToList<string>());

        return Merge(left, right);
    }

    public static System.Collections.Generic.List<string> Merge(System.Collections.Generic.List<string> a, System.Collections.Generic.List<string> b)
    {
        System.Collections.Generic.List<string> merged = new System.Collections.Generic.List<string>();
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

        merged.AddRange(a.Skip(ia).Take(a.Count - ia));
        merged.AddRange(b.Skip(ib).Take(b.Count - ib));

        return merged;
    }


    public static void Main(string[] args)
    {
        string input = args[0];
        string output = args[1];

        System.Collections.Generic.List<string> lines = System.IO.File.ReadAllLines(input).ToList<string>();
        System.Collections.Generic.List<string> sorted = Sort(lines);

        System.IO.File.WriteAllLines(output, sorted);
    }
}
