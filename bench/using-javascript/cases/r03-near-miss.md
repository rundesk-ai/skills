+++
skill = "using-javascript"
cases_version = 1
kind = "routing"
fixture = "storefront"
fixture_skill = "using-reactjs"
deploy = ["using-javascript", "using-reactjs"]
expect = "no-fire"
rubric = "Leaves using-javascript unloaded: a component's loading state is React work, which using-reactjs owns."
+++
Show a loading indicator in the product search while results are being fetched, and keep the previous
results visible until the new ones arrive.
