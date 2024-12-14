class IONumber
{
    public static int ReadValue(string path)
    {
        try
        {
            string contents = File.ReadAllText(path);
            return int.Parse(contents);
        }
        catch
        {
            return 0;
        }
    }

    public static void WriteValue(string path, int value)
    {
        File.WriteAllText(path, value.ToString());
    }

    public static void Run(int count, string path)
    {
        File.Delete(path);

        int value = 0;
        while (value != count)
        {
            value = ReadValue(path);
            WriteValue(path, value + 1);
        }
    }

    public static void Main(string[] args)
    {
        int count = int.Parse(args[0]);
        string path = args[1];

        IONumber.Run(count, path);
    }
}