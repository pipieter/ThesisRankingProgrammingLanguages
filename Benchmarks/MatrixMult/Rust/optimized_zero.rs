use std::env;

use rulinalg::matrix::Matrix;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    let size = args.get(1).unwrap().parse::<usize>()?;

    let a: Matrix<f64> = Matrix::zeros(size, size);
    let b: Matrix<f64> = Matrix::zeros(size, size);

    let c = &a * &b;
    let value = c.data().get(0).unwrap();
    println!("{}", value);
    Ok(())
}
