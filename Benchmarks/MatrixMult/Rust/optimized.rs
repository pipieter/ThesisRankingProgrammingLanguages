use std::{
    env,
    error::Error,
    fs::File,
    io::{BufRead, BufReader, BufWriter, Write},
};

use rulinalg::matrix::{BaseMatrix, Matrix};

fn read(path: &str) -> Result<Matrix<f64>, Box<dyn Error>> {
    let file = File::open(path)?;
    let mut reader: BufReader<File> = BufReader::new(file);

    let mut line = String::new();
    let _ = reader.read_line(&mut line);
    let n: usize = line.trim().parse().unwrap();

    let mut values: Vec<f64> = Vec::with_capacity(n * n);
    loop {
        line.clear();
        if reader.read_line(&mut line)? == 0usize {
            break;
        }

        let value: f64 = line.trim().parse().unwrap();
        values.push(value);
    }
    let matrix = Matrix::new(n, n, values);

    Ok(matrix)
}

fn write(matrix: &Matrix<f64>, path: &str) -> Result<(), Box<dyn Error>> {
    let file = File::create(path)?;
    let mut writer: BufWriter<File> = BufWriter::new(file);

    let n = matrix.cols();
    let nstring = format!("{}\n", n);
    let _ = writer.write(nstring.as_bytes())?;

    for i in 0..n {
        for j in 0..n {
            let line = format!("{}\n", matrix[[i, j]]);
            let _ = writer.write(line.as_bytes())?;
        }
    }

    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();

    let a = read(args.get(1).unwrap())?;
    let b = read(args.get(2).unwrap())?;

    let c = &a * &b;

    write(&c, args.get(3).unwrap())?;

    Ok(())
}
