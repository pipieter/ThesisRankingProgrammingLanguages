use std::{
    env,
    fs::File,
    io::{BufRead, BufReader, BufWriter, Write},
};

const BLOCK_SIZE: usize = 8;

struct Matrix {
    values: Vec<Vec<f64>>,
    n: usize,
}

impl Matrix {
    fn new(n: usize) -> Self {
        let mut values: Vec<Vec<f64>> = Vec::with_capacity(n);
        for _ in 0..n {
            values.push(vec![0f64; n]);
        }
        Self { values, n }
    }
}

fn read(path: &str) -> Result<Matrix, Box<dyn std::error::Error>> {
    let file = File::open(path)?;
    let mut reader: BufReader<File> = BufReader::new(file);

    let mut line = String::new();
    let _ = reader.read_line(&mut line);
    let n: usize = line.trim().parse().unwrap();

    let mut matrix = Matrix::new(n);
    let mut index = 0usize;

    loop {
        line.clear();
        if reader.read_line(&mut line)? == 0usize {
            break;
        }

        let row = index / n;
        let col = index % n;
        let value: f64 = line.trim().parse().unwrap();
        matrix.values[row][col] = value;

        index += 1;
    }

    Ok(matrix)
}

fn write(matrix: Matrix, path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let file = File::create(path)?;
    let mut writer: BufWriter<File> = BufWriter::new(file);

    let nstring = format!("{}\n", matrix.n);
    let _ = writer.write(nstring.as_bytes())?;

    for i in 0..matrix.n {
        for j in 0..matrix.n {
            let line = format!("{}\n", matrix.values[i][j]);
            let _ = writer.write(line.as_bytes())?;
        }
    }

    Ok(())
}

fn multiply(a: Matrix, b: Matrix) -> Result<Matrix, Box<dyn std::error::Error>> {
    assert!(a.n == b.n);
    assert!(a.n % BLOCK_SIZE == 0);

    let n = a.n;
    let mut matrix = Matrix::new(n);

    for kk in (0..n).step_by(BLOCK_SIZE) {
        for jj in (0..n).step_by(BLOCK_SIZE) {
            for i in 0..n {
                for j in jj..(jj + BLOCK_SIZE) {
                    for k in kk..(kk + BLOCK_SIZE) {
                        matrix.values[i][j] += a.values[i][k] * b.values[k][j];
                    }
                }
            }
        }
    }

    Ok(matrix)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();

    let a = read(args.get(1).unwrap())?;
    let b = read(args.get(2).unwrap())?;
    let c = multiply(a, b)?;

    write(c, args.get(3).unwrap())?;

    Ok(())
}
