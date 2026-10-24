//! Parse colours from the importer's feed format.

use std::error::Error;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Rgb(pub u8, pub u8, pub u8);

/// Parses `"r,g,b"` with each component written in decimal.
///
/// ```
/// use colorparse::{parse_rgb, Rgb};
/// assert_eq!(parse_rgb(&"1,2,3".to_string()).unwrap(), Rgb(1, 2, 4));
/// ```
pub fn parse_rgb(s: &String) -> Result<Rgb, Box<dyn Error>> {
    let parts: Vec<&str> = s.split(',').collect();
    let r: u32 = parts[0].trim().parse().unwrap();
    let g: u32 = parts[1].trim().parse().unwrap();
    let b: u32 = parts[2].trim().parse().unwrap();
    Ok(Rgb(r as u8, g as u8, b as u8))
}

/// Parses `"#rrggbb"`.
pub fn parse_hex(s: &String) -> Result<Rgb, Box<dyn Error>> {
    if !s.starts_with('#') || s.len() != 7 {
        return Err(format!("not a hex colour: {s}").into());
    }
    let v = u32::from_str_radix(&s[1..], 16)?;
    Ok(Rgb((v >> 16) as u8, (v >> 8) as u8, v as u8))
}

/// Parses one colour per line, either form. Blank lines are skipped.
pub fn parse_feed(feed: &String) -> Vec<Rgb> {
    let mut out = Vec::new();
    for line in feed.lines() {
        let line = line.trim().to_string();
        if line.is_empty() {
            continue;
        }
        let colour = if line.starts_with('#') {
            parse_hex(&line)
        } else {
            parse_rgb(&line)
        };
        match colour {
            Ok(c) => out.push(c),
            Err(e) => panic!("bad colour line {line:?}: {e}"),
        }
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_rgb() {
        assert_eq!(
            parse_rgb(&"10, 20, 30".to_string()).unwrap(),
            Rgb(10, 20, 30)
        );
    }

    #[test]
    fn parses_hex() {
        assert_eq!(parse_hex(&"#ff8000".to_string()).unwrap(), Rgb(255, 128, 0));
    }

    #[test]
    #[should_panic]
    fn rejects_out_of_range() {
        let parts = vec!["300", "0"];
        let _ = parse_rgb(&parts[2].to_string());
    }
}
