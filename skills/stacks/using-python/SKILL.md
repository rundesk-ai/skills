---
name: using-python
description: Use when writing, reviewing, debugging, refactoring, organizing, documenting, or testing Python code, including module and package boundaries, public APIs, naming, docstrings, typing, error handling, resource lifetimes, concurrency, measured performance, runtime-version compatibility, security-sensitive operations, and standard-library unittest. It supplies Python-specific design rules with paired good and bad patterns. Do not use for a non-Python codebase, or for database engine tuning that never touches Python code.
---

# Use Python

Write Python that is obvious at the call site, safe to import, and compatible with the repository's
declared runtime. Prefer the repository's established conventions over a competing style guide.

## Start with the repository contract

Before changing code, inspect:

- the minimum and maximum supported Python versions;
- `pyproject.toml`, formatter, linter, type-checker, and test configuration;
- nearby modules for naming, import, docstring, and class-member conventions;
- public imports, documented behavior, exceptions, and serialized data that callers may rely on.

Do not modernize syntax past the runtime floor or reformat unrelated code. For Python 3.9, use
`Optional[T]` or `Union[T, None]`; `T | None` requires Python 3.10.

Prefer a check the repository can run to an opinion. `ruff check` and a type checker find most of
what a review would argue about, and a rule code makes a finding verifiable rather than a matter of
taste. Report what the tools already flag before adding judgement of your own.

## Load focused depth

- Read [references/organization-and-naming.md](references/organization-and-naming.md) when creating,
  splitting, moving, or reviewing packages, modules, classes, functions, imports, exports, names, or
  public/internal boundaries.
- Read [references/documentation-and-comments.md](references/documentation-and-comments.md) when
  writing or reviewing module, class, function, or method docstrings; comments; annotations; TODOs;
  or API documentation.
- Read [references/testing.md](references/testing.md) for standard-library `unittest` discovery,
  assertions, cleanup, subtests, mocking, async cases, isolation, and command selection. This page
  owns Python's test mechanics; deciding which behavior and risk deserve a test is a separate,
  language-neutral concern.
- Read [references/documented-traps.md](references/documented-traps.md) when reviewing unfamiliar
  code, debugging behavior nobody can explain, or checking a change against the failures Python's own
  FAQ and the ecosystem's linters have already catalogued.
- Read [references/anti-patterns.md](references/anti-patterns.md) when reviewing design rather than
  correctness: abstraction, interfaces, error-handling shape, idiom, state, and the cost each choice
  imposes later. Traps are defects; these are judgements, and the page says how to rank them.
- Read [references/typing.md](references/typing.md) when adding or reviewing annotations, choosing
  between `Protocol`, `TypedDict`, `Literal`, and a dataclass, or configuring a type checker.
- Read [references/security.md](references/security.md) when code runs a subprocess, deserializes,
  handles secrets or credentials, builds a query or a path from input, or parses untrusted data.
- Read [references/advanced-patterns.md](references/advanced-patterns.md) only for concurrency,
  cancellation, shared state, memory, or measured performance work.
- Read [references/sources.md](references/sources.md) when reviewing, updating, or challenging a
  technical claim in this skill.

## Review in risk order

1. Preserve the public contract and supported Python versions.
2. Make ownership, state changes, errors, and resource lifetimes explicit.
3. Keep imports free of unintended work and dependency direction understandable.
4. Choose names and boundaries that explain the domain without comments.
5. Apply local formatting and tooling last; style cannot repair a confused contract.

## Handle errors at the right boundary

Catch only exceptions the current layer can resolve, translate, or record. Keep the protected block
narrow and preserve the cause when translating:

```python
# Good: one operation can produce the translated failure.
try:
    payload = json.loads(raw_payload)
except json.JSONDecodeError as exc:
    raise ConfigError("Configuration is not valid JSON.") from exc

# Bad: unrelated defects are hidden and reported as missing data.
try:
    payload = json.loads(raw_payload)
    return build_config(payload)
except Exception:
    return None
```

Do not catch `Exception` at ordinary helper boundaries. A process, worker, or request isolation
boundary may catch broadly only when it records the failure and applies an explicit recovery policy.

## Make resource ownership visible

Acquire and release files, locks, transactions, temporary directories, and executors through a
context manager or an equally explicit owner:

```python
# Good
with path.open(encoding="utf-8") as stream:
    return stream.read()

# Bad: an exception before close leaks the resource.
stream = path.open(encoding="utf-8")
content = stream.read()
stream.close()
return content
```

## Prefer readable language features

Use a comprehension when it expresses one clear transform with at most a simple filter. Expand
nested loops, multiple filters, side effects, or exception handling into statements.

```python
# Good
active_names = [user.name for user in users if user.is_active]

# Bad: dense control flow disguised as an expression.
pairs = [(x, y) for x in xs for y in ys if x != y if allowed(x, y)]
```

Never use a mutable or time-dependent default value:

```python
# Good
from typing import Optional


def collect(item: str, items: Optional[list[str]] = None) -> list[str]:
    result = [] if items is None else items
    result.append(item)
    return result

# Bad: every call shares the same list.
def collect(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items
```

## Write it once, for a reader that exists

Duplication and dead code arrive one reasonable edit at a time, often from different agents each
revising code they did not write, and every copy is a place the next fix misses:

- **Before writing a formula, threshold, tolerance, lookup or list of cases, search for it by its
  inputs**, not by the name you would give it: a copy someone else wrote has another name or none.
  Found, call it; not found, give it one home beside its inputs.
- **Never copy a function to change one value or one end**; take the difference as a parameter.
  Copies that already disagree are a bug: decide which is right and prove it with a test.
- **A view, preview, command or test helper calls the model's rule and reads its state**; it never
  re-derives them or keeps its own copy.
- **Add an output in the same change as the code that reads it.** A field, key, option or parameter
  nothing reads is dead on arrival, and a test that only exercises it is not a reader. A parameter
  every caller passes the same value is a constant.
- **A comment names only what exists in this repository**: no task or phase id, no document from
  another project, no function that is not there. Those go stale the day they are written.
- **Leave nothing your change made unused.** When new code replaces old, delete the old in the same
  change, then every helper, test, asset (icon, image, sound, scene), configuration key and string only
  it used, until nothing new is unused. Anything that was already unused, list in your hand-off for the
  owner to decide rather than deleting it: it may be kept on purpose. Before finishing, read your diff:
  every new name has a reader.

Two or three repeated lines, or one number meaning two things, are not duplication. Ruff's default
rules catch an unused import or local, not an unused function, method, attribute or argument (the
`ARG` rules are opt-in), so a `_`-prefixed name is proved unused by searching its module, and a public
one by searching every caller, entry points and configuration included.

## Keep changes proportionate

Do not introduce decorators, metaclasses, descriptors, generic frameworks, or concurrency merely to
reduce a few lines. Add an abstraction when it gives one name and one owner to behavior already
repeated or independently meaningful.
