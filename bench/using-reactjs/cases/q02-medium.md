+++
skill = "using-reactjs"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "storefront"
rubric = """
result.1  Finds the race: the effect applies every response with no cleanup, so a slow response for an earlier query overwrites the newer one; fixes with a cleanup that ignores or aborts stale requests (an ignore flag, `AbortController`, or a data library that does this).
result.2  Finds that `count` is derived state copied in an effect, so it renders one commit behind `results`; deletes the state and the effect and derives it during render.
result.3  Finds that clearing the box leaves the previous results on screen (`if (!query) return` keeps stale state), and derives an empty result for an empty query.
result.4  Adds a test that resolves two requests out of order and asserts the newer results win; it fails before the fix and passes after, with the rest of the suite.
result.5  Handles a rejected search (error state or at least no unhandled rejection), or states that it is left out.
conduct.1 Reproduces the stale result before changing code.
conduct.2 Reports each cause separately with what proves it fixed.
"""
+++
The product search sometimes shows results for something I typed earlier instead of what's in the box,
and the "N results" line seems to lag. Fix it.
