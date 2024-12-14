
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

class SetSort {
    public static void Sort(String in, String out) throws IOException, FileNotFoundException {
        Set<Integer> set = new HashSet<Integer>();

        // Read file
        {
            try (BufferedReader reader = new BufferedReader(new FileReader(in))) {
                String line = reader.readLine();
                while (line != null) {
                    int value = Integer.parseInt(line);
                    set.add(value);
                    line = reader.readLine();
                }
            }
        }

        // Write file
        {
            Integer[] array = set.toArray(Integer[]::new);
            Arrays.sort(array);
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(out))) {
                for (Integer value : array) {
                    writer.write(value.toString());
                    writer.newLine();
                }
            }
        }
    }

    public static void main(String[] args) throws FileNotFoundException, IOException {
        String in = args[0];
        String out = args[1];

        SetSort.Sort(in, out);
    }
}
