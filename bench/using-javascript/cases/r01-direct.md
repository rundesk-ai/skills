+++
skill = "using-javascript"
cases_version = 1
kind = "routing"
fixture = "orders"
deploy = ["using-javascript", "using-reactjs"]
expect = "fire"
rubric = "Loads using-javascript for a TypeScript conversion of a Node module; using-reactjs stays unloaded."
+++
Convert src/feed.js to TypeScript with strict compiler settings, and make sure it type-checks.
