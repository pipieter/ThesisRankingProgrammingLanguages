class SetSorter
{
    public static void SetSort(string inPath, string outPath)
    {
        HashSet<int> set = [];

        // Read set
        {
            using StreamReader reader = new(inPath);
            string? line = reader.ReadLine();

            while (line != null)
            {
                set.Add(int.Parse(line));
                line = reader.ReadLine();
            }
        }

        // Write set
        {
            using StreamWriter writer = new(outPath);
            List<int> list = [.. set];
            list.Sort();

            foreach (int value in list)
            {
                writer.WriteLine(value);
            }
        }
    }

    public static void Main(string[] args)
    {
        string inPath = args[0];
        string outPath = args[1];

        SetSorter.SetSort(inPath, outPath);
    }
}