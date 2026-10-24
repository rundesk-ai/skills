+++
skill = "using-rust"
cases_version = 1
kind = "routing"
fixture = "userd"
expect = "fire"
rubric = "Loads the skill even though the request never says Rust."
+++
I added a retry to fetch_user in src/main.rs and now the build fails with some Send error at
tokio::spawn. Get it building again.
