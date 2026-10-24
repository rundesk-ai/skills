+++
skill = "using-reactjs"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "storefront"
rubric = """
result.1  Names the cause: rows are keyed by array index, so after a removal the next item takes over the removed row's component and its `qty` state.
result.2  Fixes it with a stable key from the data (`item.id`) and removes by id rather than by index.
result.3  Notices that each row's quantity is local state seeded once from `item.qty` (so the cart never learns the edited quantity) and either lifts it to the cart or states that limitation.
result.4  Adds a test that types a quantity, removes another item, and asserts the remaining rows keep their own quantities; it fails before the fix and the suite passes after.
conduct.1 Reproduces the wrong behaviour before changing code.
conduct.2 Runs `npm test` and reports its output.
"""
+++
If I change the quantity of the first item in my cart and then remove that item, the quantity I typed
shows up on the next product instead. Fix it.
