namespace MergeSort;


public class MergeSorter
{
    public static List<List<string>> SplitBlocks(string path, int blockSize)
    {
        int bytesRead = 0;

        List<List<string>> blocks = [];
        List<string> lines = [];

        StreamReader reader = new(new FileStream(path, FileMode.Open));

        string? line = reader.ReadLine();
        while (line != null)
        {
            lines.Add(line);
            bytesRead += line.Length;

            if (bytesRead >= blockSize)
            {
                // Sort in reverse order
                lines.Sort(StringComparer.Ordinal);
                lines.Reverse();

                blocks.Add(lines);

                lines = [];
                bytesRead = 0;
            }

            line = reader.ReadLine();
        }

        if (lines.Count > 0)
        {
            lines.Sort(StringComparer.Ordinal);
            lines.Reverse();
            blocks.Add(lines);
        }

        return blocks;
    }

    public static List<string> MergeBlocks(List<List<string>> blocks)
    {
        List<string> sorted = [];

        while (true)
        {
            int lowestIndex = -1;
            for (int i = 0; i < blocks.Count; i++)
            {
                if (blocks[i].Count == 0)
                    continue;

                else if (lowestIndex == -1)
                    lowestIndex = i;

                else
                {
                    string current = blocks[lowestIndex].Last();
                    string value = blocks[i].Last();
                    if (string.CompareOrdinal(current, value) > 0)
                    {
                        lowestIndex = i;
                    }
                }
            }

            if (lowestIndex == -1)
                break;

            string lowest = blocks[lowestIndex].Last();
            blocks[lowestIndex].RemoveAt(blocks[lowestIndex].Count - 1);
            sorted.Add(lowest);
        }

        return sorted;
    }


    public static void Main(string[] args)
    {
        if (args.Length < 3)
        {
            Console.Error.WriteLine("Invalid arguments. Expected three arguments");
            return;
        }

        string file = args[0];
        string outFile = args[1];
        int blockSize = int.Parse(args[2]);

        var blocks = SplitBlocks(file, blockSize);
        var sorted = MergeBlocks(blocks);

        using StreamWriter writer = new(outFile);
        foreach (string line in sorted)
        {
            writer.WriteLine(line);
        }
    }
}
