import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;

public class Optimized {
    public static String[] Sort(String[] entries) {
        if (entries.length <= 1) {
            return entries;
        }

        int half = entries.length / 2;

        String[] left = new String[half];
        String[] right = new String[entries.length - half];

        System.arraycopy(entries, 0, left, 0, half);
        System.arraycopy(entries, half, right, 0, entries.length - half);

        String[] leftSorted = Sort(left);
        String[] rightSorted = Sort(right);

        return Merge(leftSorted, rightSorted);
    }

    public static String[] Merge(String[] a, String[] b) {
        String[] merged = new String[a.length + b.length];
        int i = 0;
        int ia = 0;
        int ib = 0;

        while (ia < a.length && ib < b.length) {
            if (a[ia].compareTo(b[ib]) < 0) {
                merged[i] = a[ia];
                ia++;
            } else {
                merged[i] = b[ib];
                ib++;
            }
            i++;
        }

        System.arraycopy(a, ia, merged, i, a.length - ia);
        i += a.length - ia;
        System.arraycopy(b, ib, merged, i, b.length - ib);

        return merged;
    }

    public static void main(String[] args) throws IOException {
        if (args.length < 2) {
            System.err.println("Invalid arguments.");
            System.err.println("Expected: java [file in] [file out]");
            return;
        }

        String input = args[0];
        String output = args[1];

        String[] lines = Files.readAllLines(new File(input).toPath()).toArray(String[]::new);
        String[] sorted = Sort(lines);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(output))) {
            for (String string : sorted) {
                writer.write(string);
                writer.newLine();
            }
        }
    }
}