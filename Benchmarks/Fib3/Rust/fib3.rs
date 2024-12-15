fn fib3(value: i64) -> i64 {
    if value == 0 {
        return 0i64;
    }
    if value == 1 {
        return 1i64;
    }
    if value == 2 {
        return 1i64;
    }

    fib3(value - 1) + fib3(value - 2) + fib3(value - 3)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();

    let value = args.get(1).unwrap().parse::<i64>().unwrap();
    let result = fib3(value);

    println!("{}", result);
}
