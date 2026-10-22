+++
skill = "using-rust"
kind = "routing"
fixture = "pystats"
expect = "no-fire"
rubric = "Fixes the Python fallback without loading the Rust skill; the Rust extension is untouched."
+++
The reporting job blew up on an empty batch: `python3 -m unittest discover -s tests -t .` shows
test_empty_report failing with ZeroDivisionError in stats.py. Fix it so an empty batch gives the
summary the test expects.
