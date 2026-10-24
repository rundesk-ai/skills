+++
skill = "using-tauri"
cases_version = 1
kind = "routing"
fixture = "tempconv"
expect = "no-fire"
rubric = "Fixes the integer-division bug in the plain Rust CLI without loading the Tauri skill."
+++
`cargo test` fails on room_temperature: tempconv says 70f is 21.0C, it should be 21.1C. Fix it.
