use std::{
    fs::File,
    io::{BufRead, BufReader, Write},
};

fn split_blocks(path: String, block_size: i32) -> Vec<Vec<String>> {
    let mut bytes_read: i32 = 0;

    let mut blocks: Vec<Vec<String>> = Vec::new();
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
            lines.reverse();

            blocks.push(lines.clone());

            lines.clear();
            bytes_read = 0;
        }
    }

    if !lines.is_empty() {
        lines.sort();
        lines.reverse();

        blocks.push(lines.clone());
    }

    blocks
}

fn merge_blocks(blocks: &mut Vec<Vec<String>>) -> Vec<String> {
    let mut sorted: Vec<String> = Vec::new();

    loop {
        let mut current_index: Option<usize> = None;

        for i in 0..blocks.len() {
            let block = blocks.get(i).unwrap();

            if block.is_empty() {
                continue;
            }

            if current_index.is_none() {
                current_index = Some(i);
            } else {
                let current = blocks
                    .get(current_index.unwrap())
                    .unwrap()
                    .into_iter()
                    .last()
                    .unwrap();
                let next = blocks.get(i).unwrap().into_iter().last().unwrap();

                if next < current {
                    current_index = Some(i);
                }
            }
        }
        if current_index.is_none() {
            break;
        }

        let current = blocks
            .get_mut(current_index.unwrap())
            .unwrap()
            .pop()
            .unwrap()
            .to_string();
        sorted.push(current);
    }

    sorted
}

fn main() {
    let args: Vec<String> = std::env::args().collect();

    let file = args.get(1).unwrap().to_string();
    let out = args.get(2).unwrap().to_string();
    let block_size = args.get(3).unwrap().parse::<i32>().unwrap();

    let blocks = split_blocks(file, block_size);
    let sorted = merge_blocks(&mut blocks.clone());

    let mut file = File::create(&out).unwrap();
    for value in sorted {
        let _ = file.write(value.as_bytes());
    }

}
