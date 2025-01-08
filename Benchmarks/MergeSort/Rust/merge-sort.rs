use std::{
    fs::File,
    io::{BufRead, BufReader, BufWriter, Write},
};

fn merge_sort(entries: &[String]) -> Vec<String> {
    if entries.len() <= 1 {
        return entries.to_vec();
    }

    let half = entries.len() / 2;
    let left = merge_sort(&entries[0..half]);
    let right = merge_sort(&entries[half..entries.len()]);

    merge(&left, &right)
}

fn merge(a: &[String], b: &[String]) -> Vec<String> {
    let mut merged: Vec<String> = Vec::with_capacity(a.len() + b.len());
    let mut ia = 0;
    let mut ib = 0;

    while ia < a.len() && ib < b.len() {
        if a[ia] < b[ib] {
            merged.push(a[ia].clone());
            ia += 1;
        } else {
            merged.push(b[ib].clone());
            ib += 1;
        }
    }

    for i in ia..a.len() {
        merged.push(a[i].clone());
    }
    for i in ib..b.len() {
        merged.push(b[i].clone());
    }

    merged
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

    let sorted = merge_sort(&lines);

    let mut out = BufWriter::new(File::create(&output).unwrap());
    for line in sorted {
        let _ = writeln!(out, "{}", line);
    }
}
