use std::{
    env,
    error::Error,
    fs::{self, read_to_string, File},
    io::Write,
};

fn read_value(path: &str) -> i32 {
    let value = read_to_string(path);
    if value.is_ok() {
        let parsed = value.unwrap().parse::<i32>();
        if parsed.is_ok() {
            return parsed.unwrap();
        }
    }
    0i32
}

fn write_value(path: &str, value: i32) -> Result<(), Box<dyn Error>> {
    let mut file = File::create(path)?;
    let _ = file.write_all(value.to_string().as_bytes());

    Ok(())
}

fn run(count: i32, path: &str) -> Result<(), Box<dyn Error>> {
    fs::remove_file(path)?;

    let mut value = 0;
    while value != count {
        value = read_value(path);
        write_value(path, value + 1)?;
    }

    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();

    let count = args.get(1).unwrap().parse::<i32>()?;
    let path = args.get(2).unwrap();

    run(count, path)
}
