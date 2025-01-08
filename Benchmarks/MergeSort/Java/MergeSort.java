
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;

class MergeSort {
    public static ArrayList<String> Sort(List<String> entries) {
        if (entries.size() <= 1) {
            return new ArrayList<String>(entries);
        }

        int half = entries.size() / 2;
        ArrayList<String> left = Sort(entries.subList(0, half));
        ArrayList<String> right = Sort(entries.subList(half, entries.size()));

        return Merge(left, right);
    }

    public static ArrayList<String> Merge(List<String> a, List<String> b) {
        ArrayList<String> merged = new ArrayList<>();
        int ia = 0;
        int ib = 0;

        while (ia < a.size() && ib < b.size()) {
            if (a.get(ia).compareTo(b.get(ib)) < 0) {
                merged.add(a.get(ia));
                ia++;
            } else {
                merged.add(b.get(ib));
                ib++;
            }
        }

        merged.addAll(a.subList(ia, a.size()));
        merged.addAll(b.subList(ib, b.size()));

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

        List<String> lines = Files.readAllLines(new File(input).toPath());
        List<String> sorted = Sort(lines);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(output))) {
            for (String string : sorted) {
                writer.write(string);
                writer.newLine();
            }
        }
    }
}
