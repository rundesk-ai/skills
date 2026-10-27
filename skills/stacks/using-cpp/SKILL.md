---
name: using-cpp
description: Use when writing, reviewing, debugging, organizing, or building C++, including ownership and lifetime, undefined behavior, header and translation-unit organization, toolchains and CMake targets, warnings, sanitizers, stale or wrong build artifacts, and platform variation. It supplies modern C++ defaults, the failures each one prevents, and an evidence-first workflow. Do not use it for C, or for another language that merely links a C++ library.
---

# Use C++

Make ownership visible, lifetimes defensible, and builds reproducible.

## Establish the environment

Read the build before changing source:

```sh
c++ --version
rg --files -uuu -g 'compile_commands.json'
test ! -f CMakeLists.txt || cmake --version
test ! -f CMakeLists.txt || rg 'CXX_STANDARD|cxx_std_|CMAKE_CXX_FLAGS' -g 'CMakeLists.txt'
```

Confirm the compiler, generator, standard floor, and exact command in `compile_commands.json` when
available. For a non-CMake project, inspect its active build configuration rather than translating
it into CMake. Do not introduce a newer language feature or raise the floor without approval.

## Work in this order

1. Establish who owns each resource and when it dies.
2. Reproduce the failure; confirm the edited file and launched binary belong to the same build.
3. Enable compiler warnings and the relevant sanitizer before debugging suspected lifetime, UB, or
   race failures by inspection.
4. Fix correctness, then profile before changing code for performance.
5. Run the smallest relevant test, then the wider suite.

## Defaults and failure modes

| Prefer | Avoid | Failure prevented |
|---|---|---|
| RAII and values | naked `new` / `delete` | leaks and partial cleanup on early exit or exceptions |
| `unique_ptr` for ownership; `shared_ptr` only for shared lifetime | raw owning pointers | ambiguous deletion and reference cycles |
| rule of zero; otherwise consider the full copy/move/destructor set | one ad hoc special member | accidental copies, double deletion, or disabled moves |
| `const` where mutation is not intended | mutable-by-default state | unreviewable side effects |
| target-scoped CMake properties | directory-wide flags and includes | hidden transitive build dependencies |
| separate build directories for concurrent/configuration-specific work | concurrent writers in one Ninja tree | duplicated commands and shared build-state races |
| compiler, sanitizer, or failing-test evidence | “this looks wrong” | speculative review findings |

## Write it once, for a reader that exists

Duplication and dead code arrive one reasonable edit at a time, often from different agents each
revising code they did not write, and every copy is a place the next fix misses:

- **Before writing a formula, threshold, tolerance or lookup, search for it by its inputs**, not by
  the name you would give it: a copy someone else wrote has another name or none. Found, call it;
  not found, give it one home beside its inputs.
- **Never copy a function to change one value or one end**; take the difference as a parameter.
  Copies that already disagree are a bug: decide which is right and prove it with a test.
- **A view, preview, tool or test helper calls the model's rule**; it never re-derives it.
- **Add an output in the same change as the code that reads it.** A member, enum value or parameter
  nothing reads is dead on arrival, and a test that only exercises it is not a reader. A parameter
  every caller passes the same value is a constant.
- **A comment names only what exists in this repository**: no task or phase id, no document from
  another project, no function that is not there. Those go stale the day they are written.
- **Leave nothing your change made unused.** When new code replaces old, delete the old in the same
  change, then every helper, test, asset (icon, image, sound, scene), configuration key and string only
  it used, until nothing new is unused. Anything that was already unused, list in your hand-off for the
  owner to decide rather than deleting it: it may be kept on purpose. Before finishing, read your diff:
  every new name has a reader.

Two or three repeated lines, or one number meaning two things, are not duplication. `-Wall -Wextra`
reports an unused parameter and an unused function with internal linkage, and clang an unused private
field (`-Wunused-private-field`); nothing reports an unused function with external linkage. Put
file-local helpers in an anonymous namespace so the compiler can see them, and search every caller of
anything in a header.

## Read only what the task needs

- Creating targets or changing CMake: [project setup](references/project-setup.md).
- Splitting headers, source, or layers: [organization](references/organization.md).
- Designing owners, views, RAII, or moves: [ownership and lifetime](references/ownership-and-lifetime.md).
- Investigating optimizer-sensitive or impossible behavior: [undefined behavior](references/undefined-behavior.md).
- Configuring diagnostics or debugging a process: [tooling](references/tooling.md).
- Investigating stale, overbuilt, or wrong artifacts: [build-loop traps](references/build-loop-traps.md).
- Reviewing broadly: [anti-pattern checklist](references/anti-patterns.md).
- Auditing a technical claim: [source basis](references/sources.md).

When the code lives inside a game engine, follow the engine's own guidance for its build tool,
reflection, object lifetime and modules. The C++ language, CMake, and the build loop are covered here
either way.

## Report reproducible findings

```text
[HIGH] Dangling vector element reference
Location: src/world/Grid.cpp:88
Evidence: push_back changes capacity before the saved reference is read; ASan reports
heap-use-after-free in the reproducer.
Fix: return a value or stable handle, or resolve an index after mutation.
Check: rerun the growth case under ASan.
```

Separate defects from preferences. Report the language rule or observed diagnostic, the triggering
path, and a check for the fix.
