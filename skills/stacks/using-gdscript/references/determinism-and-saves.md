# Determinism and saves

A replay or a mid-game save is correct only when a test proves it: run to tick N, save, load, run both
to tick M, and compare a digest that covers per-cell and per-agent state, not totals that two different
worlds can share. Then break something on purpose and watch the test fail.

## Randomness

`randi`, `randf`, `seed`, `Array.shuffle` and `Array.pick_random` all draw from one global generator, so a
particle effect or a UI animation that draws a number shifts the simulation. Give each system its own
generator and save both properties:

```gdscript
var rng := RandomNumberGenerator.new()

func save_rng() -> Dictionary:
	return {"seed": rng.seed, "state": rng.state}

func load_rng(d: Dictionary) -> void:
	rng.seed = d["seed"]      # setting seed resets state, so set it first
	rng.state = d["state"]
```

- Shuffle with your own Fisher–Yates over `rng.randi_range`, not `Array.shuffle()`.
- `randi_range(a, b)` includes `b`.
- The algorithm is documented as an implementation detail, so a seed may not regenerate the same world
  after an engine upgrade. A save that must survive one stores the generated world, not only its seed.
- Neighbouring seeds can give similar streams. Derive a chunk's seed by hashing the world seed and the
  chunk coordinate, not by adding them.

## Order

- **Dictionaries iterate in insertion order**, and erasing then re-adding a key moves it to the end. Two
  dictionaries that compare equal can iterate differently and hash differently. Sort the keys before
  anything order-sensitive.
- **`sort()` and `sort_custom()` are not stable.** End every ordering in a unique tie-break.
- `hash()` is not a stable identity for saves or networking; use your own hash or `sha256_text`.

## Numbers

- GDScript `float` is 64-bit; `Vector2`, `Vector3` and `PackedFloat32Array` are 32-bit in official
  builds. `Vector2(0.1, 0).x == 0.1` is false, and above 16,777,216 a `Vector2` loses whole units. Keep
  authoritative state in `int` or `float` and make vectors for display.
- `int` wraps at 2^63; `Vector2i` and `PackedInt32Array` at 2^31, silently.
- Integer division by zero is a `SCRIPT ERROR` that aborts the whole function — a population ratio with
  an empty city kills the tick. Float division gives `inf`.
- Converting float to int truncates toward zero everywhere, including into typed containers:
  `Vector2i(Vector2(1.9, -1.9))` is `(1, -1)`. Map a position to a tile with `floori`, `Vector2i(p.floor())`
  or `>>` for a power-of-two size.

## Formats

| Format | Integers | Floats | Notes |
|---|---|---|---|
| `JSON.stringify` / `parse_string` | come back as `float`; above 2^53 lose precision; object keys come back as `String` | about 14 significant digits unless `full_precision` (the fourth argument) is `true` | `parse_string` returns `null` and logs on bad input; `JSON.new().parse()` gives the error line |
| `str()`, `"%s" %` | exact | about 14 digits: `float(str(x)) == x` can be false | not a save format |
| `var_to_str` / `str_to_var` | exact | exact | readable; keeps `Vector2i`; **`str_to_var` builds objects from text, so never for untrusted input** |
| `var_to_bytes` / `FileAccess.store_var` | exact | exact | compact; leave `full_objects` false unless the file is trusted |

After a JSON load, convert at the boundary: `int(v)` for every integer field, or `typed.assign(parsed)`
into a typed collection. `1` and `1.0` are different Dictionary keys, and `match` does not match a float
against an integer pattern, so unconverted JSON data misses every int-keyed table without an error.
`int("12abc")` is `12` and `int("abc")` is `0`; check `is_valid_int()` on text input.

**Enums are saved as plain ints.** Inserting or reordering a member silently changes every saved game,
scene and resource that stored one. Append new members only, give explicit values, or save a
`StringName` id and map it at load.

Loading a `.tres` or `.res` from a place the player can write runs whatever script it names, so a
downloaded save or mod is code — and a save written as a custom `Resource` is also tied to its script's
path and layout, so moving the script breaks old saves. Save versioned plain data. Load untrusted data
as JSON or `bytes_to_var` (which refuses objects); `str_to_var('Object(Node, …)')` built a live node.

## Ticks

Run the simulation on a fixed step — `_physics_process`, or your own accumulator — never on
`_process(delta)`. When a frame is slow the engine runs at most `max_physics_steps_per_frame` (8) steps,
so a tick-counting simulation stays deterministic but falls behind wall time; size the tick to fit.
