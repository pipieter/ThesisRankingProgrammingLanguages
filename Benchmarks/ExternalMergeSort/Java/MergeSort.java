
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

class MergeSort {

    private static String writeBlock(ArrayList<String> lines, int index) throws IOException {
        String fileName = "block." + index + ".temp";
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            for (String _line : lines) {
                writer.write(_line);
                writer.newLine();
            }
        }
        return fileName;
    }

    public static ArrayList<String> SplitBlocks(String file, int blockSize) throws FileNotFoundException, IOException {
        int index = 0;
        int bytesRead = 0;

        ArrayList<String> files = new ArrayList<>();
        ArrayList<String> lines = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new FileReader(file));

        while (true) {
            String line = reader.readLine();
            if (line == null) {
                break;
            }

            lines.add(line);
            bytesRead += line.length();

            if (bytesRead >= blockSize) {
                Collections.sort(lines);
                String fileName = writeBlock(lines, index);

                files.add(fileName);
                lines.clear();
                bytesRead = 0;
                index += 1;
            }
        }

        // Write remaining
        if (!lines.isEmpty()) {
            Collections.sort(lines);
            String fileName = writeBlock(lines, index);
            files.add(fileName);
        }

        return files;
    }

    public static void MergeBlocks(ArrayList<String> files, String out, int blockSize) throws FileNotFoundException, IOException {
        ArrayList<MergeSortBlock> blocks = new ArrayList<>();
        for (String file : files) {
            blocks.add(new MergeSortBlock(file, blockSize));
        }

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(out))) {
            while (true) {
                int block = -1;
                String value = null;

                for (int i = 0; i < blocks.size(); i++) {
                    String blockValue = blocks.get(i).Next();
                    if (blockValue == null) {
                        continue;
                    }

                    if (value == null || blockValue.compareTo(value) < 0) {
                        block = i;
                        value = blockValue;
                    }
                }

                if (block == -1) {
                    break;
                }

                blocks.get(block).Pop();
                writer.write(value);
                writer.newLine();
            }
        }
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
            ArrayList<String> files = SplitBlocks(file, blockSize);
            MergeBlocks(files, out, blockSize / files.size());
        } catch (IOException e) {
        }
    }
}
