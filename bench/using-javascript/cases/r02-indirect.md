+++
skill = "using-javascript"
cases_version = 1
kind = "routing"
fixture = "orders"
deploy = ["using-javascript", "using-reactjs"]
expect = "fire"
rubric = "Loads using-javascript though the request never names the language: a Node script that streams a file."
+++
Add a script that writes every order in data/orders.json to stdout as CSV, so we can pipe it into
other tools. It should still work when the file is a few gigabytes.
