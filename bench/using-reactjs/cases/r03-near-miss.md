+++
skill = "using-reactjs"
cases_version = 1
kind = "routing"
fixture = "storefront"
deploy = ["using-reactjs", "using-javascript"]
expect = "no-fire"
rubric = "Leaves using-reactjs unloaded: retrying a failed HTTP call in a plain module is JavaScript work that never touches a component."
+++
Make searchProducts in src/api.js retry up to two times with exponential backoff when the server
answers 502, 503 or 504, and give up immediately on other errors. Add a test for it.
