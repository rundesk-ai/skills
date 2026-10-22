# Typing and warnings

## Declarations

```gdscript
var speed: float = 4.0            # explicit
var direction := Vector2.ZERO     # inferred; the type is visible on the line
var health := 0                   # Bad: int or float? write the type
@onready var _label: Label = $Label   # explicit; := here would infer Node from get_node()
func damage(amount: int, source: Node = null) -> void:
```

Use `:=` only where the right-hand side states its type. Inferring from a `Variant` is an error by
default (`INFERENCE_ON_VARIANT`).

## Collections

- `Array[T]` types the `for` variable, literals, `[]=` and `+`; `push_back` and `==` stay untyped.
- `Dictionary[K, V]` (4.4+) needs both types; write `Variant` to leave one open. Writes are checked at
  runtime.
- Nested typed collections (`Array[Array[int]]`) do not exist; type the outer one, or wrap the inner in
  a class.
- A plain `Array` is not assignable to `Array[T]`, and `as` does not convert it. `typed.assign(plain)`
  converts element by element; a bad element logs an error and leaves `typed` unchanged.
- Typed `for` variables (4.2+): `for enemy: Enemy in enemies:`.
- Variadic rest parameters (4.5+) are `...args: Array`; they cannot be `Array[int]`, and there is no
  spread — pass an array to `callv`.

## Casts and checks

```gdscript
# Bad: body is null if it is not an Enemy, and the next line errors far from the cause
var enemy := body as Enemy
enemy.hit()

# Good
if body is Enemy:
	(body as Enemy).hit()
```

`as` to an object type gives `null` on mismatch; `as` to a built-in type that cannot convert is an error.
`is not` exists. A green "safe" line number means the parser could check the types, not that the value
cannot be `null`.

## Warnings

Warnings are set per project under `debug/gdscript/warnings/` in `project.godot`: `0` ignore, `1` warn,
`2` error. A warning raised to error stops the script from parsing, which is the only way a warning
reaches a headless check — at `1` it appears in the editor and nowhere else.

Worth raising on a project that is already typed, with the owner's agreement, since every existing
violation becomes a parse error:

| Setting | Catches |
|---|---|
| `untyped_declaration` | any variable, parameter or return without a type |
| `unsafe_property_access`, `unsafe_method_access`, `unsafe_call_argument`, `unsafe_cast` | access the parser cannot type-check |
| `integer_division` | `int / int` truncating |
| `return_value_discarded` | ignoring an `Error` or result |
| `missing_await` (4.6+) | calling a coroutine without `await` |

```ini
[debug]

gdscript/warnings/untyped_declaration=2
gdscript/warnings/integer_division=2
```

Third-party code under `res://addons` is excluded from warnings by default; `directory_rules` (4.6+)
changes which directories count. Silence one deliberate case with `@warning_ignore("integer_division")`
on the line above, or a region between `@warning_ignore_start(...)` and `@warning_ignore_restore(...)`
(4.4+). A suppression without a comment saying why is a warning hidden, not handled.

## Typed global functions

`abs`, `clamp`, `lerp`, `min`, `max`, `sign`, `snapped`, `round` take and return `Variant`. Their typed
forms — `absf`/`absi`, `clampf`/`clampi`, `lerpf`, `minf`/`mini`, `maxf`/`maxi`, `signf`/`signi`,
`snappedf`/`snappedi`, `roundi` — keep the line typed and fast.
