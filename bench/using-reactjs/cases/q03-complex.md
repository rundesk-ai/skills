+++
skill = "using-reactjs"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "storefront"
rubric = """
result.1  Measures before changing anything, with a realistic catalog (thousands of products): commits and render time while idle and per keystroke (React `<Profiler>`, the DevTools profiler, or render counts), and reports the numbers.
result.2  Finds the idle work: `now` ticks every 250 ms in `Dashboard` state and travels in the context value, so every row re-renders four times a second; and the price store rebroadcasts every second while the subscriber stores a fresh copy (`{ ...priceStore.get() }`), which renders even when nothing changed.
result.3  Fixes the structure rather than memoizing around it: the clock's state moves into `Clock`; `now` leaves the shared context (split it, or memoize a value that excludes it); prices are read with `useSyncExternalStore` returning the store's own reference, so an unchanged rebroadcast renders nothing.
result.4  Addresses keystroke cost after measuring it: a new `Intl.NumberFormat` per row per render, every row re-rendering on each keystroke, and, for thousands of rows, a deferred filter value or virtualization.
result.5  Reports before and after numbers with the same method, keeps behaviour (existing tests pass), and adds a check that would fail if idle re-rendering came back (for example zero commits over idle seconds with unchanged prices).
result.6  States the limits: numbers from jsdom or a development build are not production browser timings; says what a production profile would still need to confirm.
conduct.1 Takes numbers first; does not wrap everything in `memo`/`useMemo`/`useCallback` on appearance.
"""
+++
With our full catalog loaded, typing in the dashboard's filter box is sluggish, and the page keeps
burning CPU even when nobody touches it. Make it fast.
