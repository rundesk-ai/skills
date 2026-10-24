//! Per-endpoint statistics from the gateway's access log.
//!
//! A line looks like `2026-10-01T12:00:00Z GET /api/orders 200 512 37`: timestamp, method, path,
//! status, response bytes, latency in milliseconds.

use std::collections::HashMap;
use std::io::BufRead;

use regex::Regex;

#[derive(Debug, Clone, PartialEq)]
pub struct EndpointStats {
    pub endpoint: String,
    pub requests: u64,
    pub errors: u64,
    pub bytes: u64,
    pub p95_ms: u64,
}

pub struct Record {
    pub method: String,
    pub path: String,
    pub status: u16,
    pub bytes: u64,
    pub latency_ms: u64,
}

pub fn line_regex() -> Regex {
    Regex::new(r"^(\S+) (\S+) (\S+) (\d{3}) (\d+) (\d+)$").unwrap()
}

pub fn parse_line(re: &Regex, line: &str) -> Option<Record> {
    let caps = re.captures(line)?;
    Some(Record {
        method: caps[2].to_string(),
        path: caps[3].to_string(),
        status: caps[4].parse().ok()?,
        bytes: caps[5].parse().ok()?,
        latency_ms: caps[6].parse().ok()?,
    })
}

/// Reads the whole log and returns one row per endpoint, busiest first.
pub fn summarize<R: BufRead>(input: R) -> Vec<EndpointStats> {
    let mut latencies: HashMap<String, Vec<u64>> = HashMap::new();
    let mut totals: HashMap<String, (u64, u64, u64)> = HashMap::new();
    let re = line_regex();
    for line in input.lines() {
        let line = line.unwrap();
        let Some(rec) = parse_line(&re, &line) else {
            continue;
        };
        let key = format!("{} {}", rec.method, rec.path);
        latencies
            .entry(key.clone())
            .or_default()
            .push(rec.latency_ms);
        let t = totals.entry(key.clone()).or_insert((0, 0, 0));
        t.0 += 1;
        if rec.status >= 500 {
            t.1 += 1;
        }
        t.2 += rec.bytes;
    }
    let mut rows = Vec::new();
    for (key, (requests, errors, bytes)) in totals.clone() {
        let mut l = latencies[&key].clone();
        l.sort();
        let idx = ((l.len() as f64) * 0.95).ceil() as usize - 1;
        rows.push(EndpointStats {
            endpoint: key.clone(),
            requests,
            errors,
            bytes,
            p95_ms: l[idx],
        });
    }
    rows.sort_by(|a, b| {
        b.requests
            .cmp(&a.requests)
            .then(a.endpoint.cmp(&b.endpoint))
    });
    rows
}
