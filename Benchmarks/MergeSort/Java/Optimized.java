import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Arrays;

public class Optimized {
    static final int ConcurrentThreshold = 10_000;

    public static void SortParallel(String[] entries)  {
        if (entries.length <= 1) {
            return;
        }

        if (entries.length < ConcurrentThreshold) {
            SortConcurrent(entries);
            return;
        }
        int half = entries.length / 2;

        String[] left = Arrays.copyOfRange(entries, 0, half);
        String[] right = Arrays.copyOfRange(entries, half, entries.length);

        Thread leftSorter = new Thread(new Runnable() {
            public void run() {
                SortParallel(left);
            }
        });
        leftSorter.start();
        SortParallel(right);
        try {
            leftSorter.join();
        } catch (InterruptedException e) {
            System.err.println("Could not finish SortParallel on left");
            System.exit(1);
        }

        Merge(left, right, entries);
    }

    public static void SortConcurrent(String[] entries) {
        if ((entries.length) <= 1) {
            return;
        }

        int half = entries.length / 2;

        String[] left = Arrays.copyOfRange(entries, 0, half);
        String[] right = Arrays.copyOfRange(entries, half, entries.length);

        SortConcurrent(left);
        SortConcurrent(right);

        Merge(left, right, entries);
    }

    public static void Merge(String[] a, String[] b, String[] target) {
        int i = 0;
        int ia = 0;
        int ib = 0;

        while (ia < a.length && ib < b.length) {
            if (a[ia].compareTo(b[ib]) < 0) {
                target[i] = a[ia];
                ia++;
            } else {
                target[i] = b[ib];
                ib++;
            }
            i++;
        }

        System.arraycopy(a, ia, target, i, a.length - ia);
        i += a.length - ia;
        System.arraycopy(b, ib, target, i, b.length - ib);
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
        SortParallel(lines);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(output))) {
            for (String string : lines) {
                writer.write(string);
                writer.newLine();
            }
        }
    }
}