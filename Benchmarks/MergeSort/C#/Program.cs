namespace MergeSort;

using System.Collections;
using System.Reflection.Metadata;

public class MergeSortBlock
{
    protected StreamReader _reader;
    protected int _blockSize;
    protected Queue<string> _queue;
    protected bool _hasRemaining;

    public MergeSortBlock(string path, int blockSize)
    {
        _reader = new StreamReader(new FileStream(path, FileMode.Open));
        _queue = [];
        _blockSize = blockSize;
        _hasRemaining = true;
    }

    public string? Next()
    {
        if (_queue.Count == 0 && _hasRemaining)
            ReadBlock();

        if (_queue.Count == 0)
            return null;

        return _queue.First();
    }

    public string Pop()
    {
        return _queue.Dequeue();
    }

    protected void ReadBlock()
    {
        if (!_hasRemaining) return;

        int dataRead = 0;
        while (dataRead < _blockSize)
        {
            string? line = _reader.ReadLine();
            if (line == null)
            {
                _hasRemaining = false;
                break;
            }
            else
            {
                _queue.Enqueue(line);
                dataRead += line.Length;
            }
        }
    }
}

public class MergeSort
{
    private static string WriteBlock(List<string> lines, int index)
    {
        string fileName = $"block.{index}.temp";
        File.WriteAllLines(fileName, lines);
        return fileName;
    }

    public static List<string> SplitBlocks(string path, int blockSize)
    {
        int index = 0;
        int bytesRead = 0;

        List<string> files = [];
        List<string> lines = [];

        StreamReader reader = new(new FileStream(path, FileMode.Open));

        while (true)
        {
            string? line = reader.ReadLine();
            if (line == null)
            {
                break;
            }

            lines.Add(line);
            bytesRead += line.Length;

            if (bytesRead >= blockSize)
            {
                lines.Sort(StringComparer.Ordinal);
                string fileName = WriteBlock(lines, index);

                files.Add(fileName);
                lines.Clear();
                bytesRead = 0;
                index++;
            }
        }

        if (lines.Count > 0)
        {
            lines.Sort(StringComparer.Ordinal);
            string fileName = WriteBlock(lines, index);
            files.Add(fileName);
        }

        return files;
    }

    public static void MergeBlocks(List<string> files, string outFile, int blockSize)
    {
        List<MergeSortBlock> blocks = [];
        foreach (string file in files)
        {
            blocks.Add(new MergeSortBlock(file, blockSize));
        }

        using StreamWriter writer = new(outFile);

        while (true)
        {
            int block = -1;
            string? value = null;

            for (int i = 0; i < blocks.Count; i++)
            {
                string? blockValue = blocks[i].Next();
                if (blockValue == null) continue;

                if (value == null || string.Compare(blockValue, value, StringComparison.Ordinal) < 0)
                {
                    block = i;
                    value = blockValue;
                }
            }

            if (block == -1)
                break;

            blocks[block].Pop();
            writer.WriteLine(value);
        }
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

        List<string> files = SplitBlocks(file, blockSize);
        MergeBlocks(files, outFile, blockSize / files.Count);
    }
}
