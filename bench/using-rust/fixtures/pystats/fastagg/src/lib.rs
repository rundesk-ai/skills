//! Aggregation kernel behind the reporting job's fast path. The Python bindings are generated at
//! release time; this crate holds only the arithmetic.

/// Returns `(count, total, max)` for a batch, or `None` for an empty one.
pub fn aggregate(values: &[i64]) -> Option<(usize, i64, i64)> {
    let max = *values.iter().max()?;
    Some((values.len(), values.iter().sum(), max))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn aggregates() {
        assert_eq!(aggregate(&[2, 4, 6]), Some((3, 12, 6)));
        assert_eq!(aggregate(&[]), None);
    }
}
