use std::{
    collections::VecDeque,
    fs::File,
    io::{BufRead, BufReader, Write},
};

struct MergeSortBlock {
    reader: BufReader<File>,
    block_size: i32,
    queue: VecDeque<String>,
    has_remaining: bool,
}

impl MergeSortBlock {
    fn new(path: &str, block_size: i32) -> MergeSortBlock {
        MergeSortBlock {
            block_size,
            reader: BufReader::new(File::open(path).unwrap()),
            queue: VecDeque::new(),
            has_remaining: true,
        }
    }
    fn next(&mut self) -> Option<String> {
        if self.queue.is_empty() && self.has_remaining {
            self.read_block();
        }

        if self.queue.is_empty() {
            return None;
        }

        self.queue.front().cloned()
    }

    fn read_block(&mut self) -> () {
        if !self.has_remaining {
            return;
        };

        let mut data_read = 0;
        while data_read < self.block_size {
            let mut line = String::new();
            let result = self.reader.read_line(&mut line);

            if result.is_err() {
                break;
            }

            let length = result.unwrap();
            if length == 0 {
                self.has_remaining = false;
                break;
            }

            self.queue.push_back(line);
            data_read += length as i32;
        }
    }

    fn pop(&mut self) -> () {
        self.queue.pop_front();
    }
}

fn write_block(lines: &Vec<String>, index: i32) -> String {
    let file_name = format!("./temp/block.{index}.temp");
    let mut file = File::create(&file_name).unwrap();

    for line in lines {
        let _ = file.write(line.as_bytes());
    }

    file_name
}

fn split_blocks(path: String, block_size: i32) -> Vec<String> {
    let mut index: i32 = 0;
    let mut bytes_read: i32 = 0;

    let mut files: Vec<String> = Vec::new();
    let mut lines: Vec<String> = Vec::new();

    let mut reader: BufReader<File> = BufReader::new(File::open(path).unwrap());

    loop {
        let mut line = String::new();
        let result = reader.read_line(&mut line);

        if result.is_err() {
            break;
        }

        let length = result.unwrap();
        if length == 0 {
            break;
        }

        lines.push(line);
        bytes_read += length as i32;

        if bytes_read >= block_size {
            lines.sort();
            let file_name = write_block(&lines, index);

            files.push(file_name);
            lines.clear();
            bytes_read = 0;
            index += 1;
        }
    }

    if !lines.is_empty() {
        lines.sort();
        let file_name = write_block(&lines, index);
        files.push(file_name);
    }

    files
}

fn merge_blocks(files: &Vec<String>, out: String, block_size: i32) -> () {
    let mut blocks: Vec<MergeSortBlock> = Vec::new();
    for file in files {
        blocks.push(MergeSortBlock::new(file, block_size));
    }

    let mut file = File::create(&out).unwrap();

    loop {
        let mut block = -1i32;
        let mut value: String = String::new();

        for i in 0..blocks.len() {
            let block_i = &mut blocks[i];
            let block_value = block_i.next();

            if block_value.is_none() {
                continue;
            }

            let block_value = block_value.unwrap();

            if value.is_empty() || block_value < value {
                block = i as i32;
                value = block_value;
            }
        }

        if block == -1 {
            break;
        }

        blocks[block as usize].pop();
        let _ = file.write(value.as_bytes());
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();

    let file = args.get(1).unwrap().to_string();
    let out = args.get(2).unwrap().to_string();
    let block_size = args.get(3).unwrap().parse::<i32>().unwrap();

    let files = split_blocks(file, block_size);
    merge_blocks(&files, out, block_size / (files.len() as i32));
}
