//! Count words in a text file and print them, most frequent first.

use std::collections::HashMap;
use std::env;
use std::fs;
use std::process::ExitCode;

fn tally(text: &str) -> Vec<(String, usize)> {
    let mut counts: HashMap<String, usize> = HashMap::new();
    for word in text.split_whitespace() {
        *counts.entry(word.to_lowercase()).or_default() += 1;
    }
    let mut rows: Vec<(String, usize)> = counts.into_iter().collect();
    rows.sort_by(|a, b| b.1.cmp(&a.1).then_with(|| a.0.cmp(&b.0)));
    rows
}

fn main() -> ExitCode {
    let Some(path) = env::args().nth(1) else {
        eprintln!("usage: wordtally <file>");
        return ExitCode::from(2);
    };
    let text = match fs::read_to_string(&path) {
        Ok(t) => t,
        Err(e) => {
            eprintln!("wordtally: {path}: {e}");
            return ExitCode::FAILURE;
        }
    };
    for (word, n) in tally(&text) {
        println!("{n:>7} {word}");
    }
    ExitCode::SUCCESS
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn most_frequent_first() {
        let rows = tally("b a b c b a");
        assert_eq!(rows[0], ("b".to_string(), 3));
        assert_eq!(rows[1], ("a".to_string(), 2));
    }
}
