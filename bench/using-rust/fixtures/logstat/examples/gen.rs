//! Writes a deterministic synthetic access log: `cargo run --release --example gen -- <lines> > access.log`

use std::io::{self, BufWriter, Write};

fn main() -> io::Result<()> {
    let lines: u64 = std::env::args()
        .nth(1)
        .and_then(|s| s.parse().ok())
        .unwrap_or(2_000_000);
    let methods = ["GET", "GET", "GET", "POST", "PUT", "DELETE"];
    let mut state: u64 = 0x9E37_79B9_7F4A_7C15;
    let mut next = move || {
        state ^= state << 13;
        state ^= state >> 7;
        state ^= state << 17;
        state
    };
    let mut out = BufWriter::new(io::stdout().lock());
    for i in 0..lines {
        let r = next();
        let method = methods[(r % 6) as usize];
        let path = format!("/api/v1/resource{}/item{}", (r >> 8) % 40, (r >> 16) % 500);
        let status = match (r >> 24) % 100 {
            0..=1 => 503,
            2..=6 => 404,
            _ => 200,
        };
        let bytes = (r >> 32) % 65_536;
        let latency = 1 + (r >> 40) % 250 + if (r >> 48) % 50 == 0 { 2_000 } else { 0 };
        writeln!(
            out,
            "2026-10-01T12:{:02}:{:02}Z {method} {path} {status} {bytes} {latency}",
            (i / 60) % 60,
            i % 60
        )?;
    }
    out.flush()
}
