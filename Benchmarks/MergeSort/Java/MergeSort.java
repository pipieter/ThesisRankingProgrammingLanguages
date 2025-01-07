
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

class MergeSort {
    public static ArrayList<ArrayList<String>> SplitBlocks(String file, int blockSize)
            throws FileNotFoundException, IOException {
        int bytesRead = 0;

        ArrayList<ArrayList<String>> blocks = new ArrayList<>();
        ArrayList<String> lines = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            while (true) {
                String line = reader.readLine();
                if (line == null) {
                    break;
                }

                lines.add(line);
                bytesRead += line.length();

                if (bytesRead >= blockSize) {
                    Collections.sort(lines, Collections.reverseOrder());

                    blocks.add(lines);

                    lines = new ArrayList<String>();
                    bytesRead = 0;
                }
            }
        }

        // Write remaining
        if (!lines.isEmpty()) {
            Collections.sort(lines, Collections.reverseOrder());
            blocks.add(lines);
        }

        return blocks;
    }

    public static ArrayList<String> MergeBlocks(ArrayList<ArrayList<String>> blocks) {
        ArrayList<String> sorted = new ArrayList<>();

        while (true) {
            int block = -1;

            for (int i = 0; i < blocks.size(); i++) {
                if (blocks.get(i).isEmpty()) {
                    continue;
                }

                if (block == -1) {
                    block = i;
                } else {
                    String current = blocks.get(block).get(blocks.get(block).size() - 1);
                    String next = blocks.get(i).get(blocks.get(i).size() - 1);

                    if (next.compareTo(current) < 0) {
                        block = i;
                    }
                }
            }

            if (block == -1) {
                break;
            }

            String value = blocks.get(block).remove(blocks.get(block).size() - 1);
            sorted.add(value);
        }

        return sorted;
    }

    public static void main(String[] args) {
        if (args.length < 3) {
            System.err.println("Invalid arguments.");
            System.err.println("Expected: java [file in] [file out] [block size]");
            return;
        }

        String file = args[0];
        String out = args[1];
        int blockSize = Integer.parseInt(args[2]);

        try {
            ArrayList<ArrayList<String>> blocks = SplitBlocks(file, blockSize);
            ArrayList<String> sorted = MergeBlocks(blocks);

            try (BufferedWriter writer = new BufferedWriter(new FileWriter(out))) {
                for (String string : sorted) {
                    writer.write(string);
                    writer.newLine();
                }
            }
        } catch (IOException e) {
        }
    }
}
