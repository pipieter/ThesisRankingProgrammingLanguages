
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Collections;
import java.util.LinkedList;

public class MergeSortBlock {

    private final BufferedReader reader;
    private final int blockSize;

    private final LinkedList<String> values;
    private boolean fileHasRemaining;

    public MergeSortBlock(String file, int blockSize) throws FileNotFoundException {
        this.reader = new BufferedReader(new FileReader(file));
        this.blockSize = blockSize;

        this.values = new LinkedList<>();
        this.fileHasRemaining = true;
    }

    public String Next() throws IOException {
        if (this.values.isEmpty() && fileHasRemaining) {
            this.readBlock();
        }

        if (!this.values.isEmpty()) {
            return this.values.get(0);
        }

        return null;
    }

    private void readBlock() throws IOException {
        if (!this.fileHasRemaining) {
            return;
        }

        values.clear();
        int bytesRead = 0;
        while (bytesRead < this.blockSize && fileHasRemaining) {
            String line = reader.readLine();
            if (line == null) {
                fileHasRemaining = false;
                break;
            } else {
                values.add(line);
                bytesRead += line.length();
            }
        }
        Collections.sort(values);
    }

    public void Pop() {
        values.removeFirst();
    }
}
