use std::{
    fs::File,
    io::{BufRead, BufReader, BufWriter, Write},
    thread,
};

const CONCURRENT_THRESHOLD: usize = 10_000usize;

fn merge_sort_parallel(entries: &mut [&String]) {
    if entries.len() < CONCURRENT_THRESHOLD {
        merge_sort_concurrent(entries);
        return;
    }

    let half = entries.len() / 2;
    let mut left = entries[0..half].to_vec();
    let mut right = entries[half..entries.len()].to_vec();

    thread::scope(|s| {
        let left_thread = s.spawn(|| {
            merge_sort_parallel(&mut left);
        });
        merge_sort_parallel(&mut right);
        left_thread.join().unwrap();
    });
    merge(&left, &right, entries);
}

fn merge_sort_concurrent(entries: &mut [&String]) {
    if entries.len() <= 1 {
        return;
    }

    let half = entries.len() / 2;
    let mut left = entries[0..half].to_vec();
    let mut right = entries[half..entries.len()].to_vec();

    merge_sort_concurrent(&mut left);
    merge_sort_concurrent(&mut right);

    merge(&left, &right, entries);
}

fn merge<'a>(a: &[&'a String], b: &[&'a String], destination: &mut [&'a String]) {
    let mut i = 0;
    let mut ia = 0;
    let mut ib = 0;

    while ia < a.len() && ib < b.len() {
        if a[ia] < b[ib] {
            destination[i] = a[ia];
            ia += 1;
        } else {
            destination[i] = b[ib];
            ib += 1;
        }
        i += 1;
    }

    while ia < a.len() {
        destination[i] = a[ia];
        ia += 1;
        i += 1;
    }
    while ib < b.len() {
        destination[i] = b[ib];
        ib += 1;
        i += 1;
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();

    let input = args.get(1).unwrap().to_string();
    let output: String = args.get(2).unwrap().to_string();

    let file = File::open(input).expect("no such file");
    let buf = BufReader::new(file);
    let lines: Vec<String> = buf
        .lines()
        .map(|l| l.expect("Could not parse line"))
        .collect();
    let mut str_lines: Vec<&String> = lines.iter().map(|v| v).collect();

    merge_sort_parallel(&mut str_lines);

    let mut out = BufWriter::new(File::create(&output).unwrap());
    for line in lines {
        let _ = writeln!(out, "{}", line);
    }
}
