# Typing and warnings

## Where typing does not reach

- On `Array[T]`, the `for` variable, literals, `[]=` and `+` are typed; `push_back` and `==` are not
  checked.
- Nested typed collections (`Array[Array[int]]`) do not exist; type the outer one, or wrap the inner in a
  class.
- Variadic rest parameters (4.5+) are `...args: Array`, never `Array[int]`.
- `as` to an object type gives `null` on mismatch; `as` to a built-in type that cannot convert is an error.
  A green "safe" line number means the parser could check the types, not that the value cannot be `null`.
- `var w := weakref(x)` does not parse: `weakref` returns `Variant`. Write `var w: WeakRef = weakref(x)`.
- Typed signal parameters are checked at dispatch, not at `emit`: `sig.emit("text")` on
  `signal sig(v: int)` parses, logs "Cannot convert argument", and the handler never runs.

## Warnings reach a headless check only as errors

Warnings are set per project under `debug/gdscript/warnings/` in `project.godot`: `0` ignore, `1` warn,
`2` error. **At `1` a warning appears in the editor and nowhere else** — not in a headless run, not in the
checker. Raising it to `2` makes it a parse error, which is the only way it reaches automation.

Worth raising on a project that is already typed, with the owner's agreement, since every existing
violation becomes a parse error:

| Setting | Catches |
|---|---|
| `untyped_declaration` | any variable, parameter or return without a type |
| `unsafe_property_access`, `unsafe_method_access`, `unsafe_call_argument`, `unsafe_cast` | access the parser cannot type-check |
| `integer_division` | `int / int` truncating |
| `missing_await` (4.6+) | calling a coroutine without `await` |

```ini
[debug]

gdscript/warnings/untyped_declaration=2
gdscript/warnings/integer_division=2
```

Code under `res://addons` is excluded from warnings by default; `directory_rules` (4.6+) changes which
directories count. Silence one deliberate case with `@warning_ignore("integer_division")` on the line
above it, with a comment saying why.

## Typed global functions

`abs`, `clamp`, `lerp`, `min`, `max`, `sign`, `snapped` and `round` take and return `Variant`, so
`var x := clamp(...)` fails to parse and an untyped result loses the static checks. Their typed forms —
`absf`/`absi`, `clampf`/`clampi`, `lerpf`, `minf`/`mini`, `maxf`/`maxi`, `signf`/`signi`,
`snappedf`/`snappedi`, `roundi` — keep the line typed and fast.
