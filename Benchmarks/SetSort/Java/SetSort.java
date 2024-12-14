
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Iterator;
import java.util.SortedSet;
import java.util.TreeSet;

class SetSort {
    public static void Sort(String in, String out) throws IOException, FileNotFoundException {
        SortedSet<Integer> values = new TreeSet<Integer>();

        // Read file
        {
            try (BufferedReader reader = new BufferedReader(new FileReader(in))) {
                String line = reader.readLine();
                while (line != null) {
                    int value = Integer.parseInt(line);
                    values.add(value);
                    line = reader.readLine();
                }
            }
        }

        // Write file
        {
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(out))) {
                Iterator<Integer> iterator = values.iterator();
                while (iterator.hasNext()) {
                    Integer value = iterator.next();
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
