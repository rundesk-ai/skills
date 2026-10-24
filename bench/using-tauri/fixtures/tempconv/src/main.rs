//! Convert temperatures: `tempconv 100c` prints 212F, `tempconv 70f` prints 21.1C.

fn convert(input: &str) -> Option<String> {
    let (num, unit) = input.split_at(input.len().checked_sub(1)?);
    let value: i32 = num.parse().ok()?;
    match unit {
        "c" | "C" => Some(format!("{}F", value * 9 / 5 + 32)),
        "f" | "F" => Some(format!("{:.1}C", ((value - 32) * 5 / 9) as f64)),
        _ => None,
    }
}

fn main() {
    for arg in std::env::args().skip(1) {
        match convert(&arg) {
            Some(out) => println!("{out}"),
            None => eprintln!("tempconv: cannot read {arg:?}"),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::convert;

    #[test]
    fn boiling() {
        assert_eq!(convert("100c").as_deref(), Some("212F"));
    }

    #[test]
    fn room_temperature() {
        assert_eq!(convert("70f").as_deref(), Some("21.1C"));
    }
}
