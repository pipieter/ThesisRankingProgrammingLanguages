use std::{
    collections::BTreeSet,
    env,
    fs::File,
    io::{BufRead, BufReader, BufWriter, Write},
};

fn set_sort(in_file: &str, out_file: &str) -> Result<(), Box<dyn std::error::Error>> {
    let mut set: BTreeSet<i32> = BTreeSet::new();

    // Read file
    {
        let file = File::open(in_file)?;
        let reader = BufReader::new(file);

        for line in reader.lines() {
            let value = line?.parse::<i32>()?;
            set.insert(value);
        }
    }

    // Write file
    {
        let file = File::create(out_file)?;
        let mut writer = BufWriter::new(file);

        for value in set {
            writer.write(value.to_string().as_bytes())?;
            writer.write("\n".as_bytes())?;
        }
    }

    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();

    let in_file = args.get(1).unwrap();
    let out_file = args.get(2).unwrap();

    set_sort(in_file, out_file)
}
