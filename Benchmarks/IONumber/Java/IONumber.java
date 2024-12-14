
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.Paths;

class IONumber {
    public static int ReadValue(String path) {
        try {
            String contents = Files.readString(Paths.get(path));
            return Integer.parseInt(contents);
        } catch (IOException e) {
            return 0;
        }
    }

    public static void WriteValue(String path, int value) throws IOException {
        Files.write(Paths.get(path), String.valueOf(value + 1).getBytes());
    }

    public static void Run(int count, String path) throws IOException {
        try {
            Files.delete(Paths.get(path));
        } catch (NoSuchFileException e) {
            // Skip
        }

        int value = 0;
        while (value != count) {
            value = ReadValue(path);
            WriteValue(path, value);
        }
    }

    public static void main(String[] args) throws FileNotFoundException, IOException {
        int count = Integer.parseInt(args[0]);
        String path = args[1];

        IONumber.Run(count, path);
    }
}
