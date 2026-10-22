+++
skill = "using-rust"
kind = "quality"
difficulty = "medium"
fixture = "colorparse"
rubric = """
result.1  Out-of-range components ("300,0,0") return an error rather than a truncated colour; the `as u8` casts are gone, replaced by `u8::try_from` or parsing straight into `u8`.
result.2  No input can panic the library: the `unwrap` calls on parsed input, the indexing of a too-short split, and the panic in `parse_feed` are all replaced by returned errors.
result.3  The public error is a type callers can match on (an error enum or struct), not `Box<dyn Error>`.
result.4  The failing doctest (`Rgb(1, 2, 4)`) is found and fixed.
result.5  Explains why CI stayed green: `cargo test --all-targets` skips doctests, and/or `#[should_panic]` without `expected` passes on any panic; fixes or flags `ci.sh`.
result.6  Parameters take `&str` rather than `&String`.
conduct.1 Runs plain `cargo test` (or `--doc`), not only `--all-targets`, before declaring done.
conduct.2 Runs clippy with `--all-targets` and treats warnings as failures.
conduct.3 Adds no dependency without stating why std is insufficient, and does not raise `rust-version` past 1.80 or the edition.
"""
+++
Support ticket from the importer team: `parse_rgb("300,0,0")` hands back some dark teal-ish colour
instead of rejecting it, and one garbage line in a feed crashes the whole importer service. Can you
fix colorparse so bad input is an error the importer can handle? CI is green, so I don't understand
how this slipped through.
