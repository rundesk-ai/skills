use std::fs::File;
use std::io::BufReader;
use std::process::ExitCode;

fn main() -> ExitCode {
    let Some(path) = std::env::args().nth(1) else {
        eprintln!("usage: logstat <access.log>");
        return ExitCode::from(2);
    };
    let file = match File::open(&path) {
        Ok(f) => f,
        Err(e) => {
            eprintln!("logstat: {path}: {e}");
            return ExitCode::FAILURE;
        }
    };
    println!("endpoint\trequests\terrors\tbytes\tp95_ms");
    for row in logstat::summarize(BufReader::new(file)) {
        println!(
            "{}\t{}\t{}\t{}\t{}",
            row.endpoint, row.requests, row.errors, row.bytes, row.p95_ms
        );
    }
    ExitCode::SUCCESS
}
