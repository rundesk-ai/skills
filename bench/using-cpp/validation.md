# Using C++ Validation

This is the current validation record for `using-cpp`; the method is
`prompts/benchmark-skill.md`.

## Boundary under test

The skill should activate for C++ language and build correctness — ownership and lifetime,
undefined behavior, header and translation-unit organization, toolchains and CMake targets,
warnings, sanitizers, stale or wrong artifacts, and platform variation. It should not activate for
C, or for a language that merely links a C++ library.

## Trigger and exclusion cases

| ID | Request shape | Expected behavior |
|---|---|---|
| CPP-T01 | Review ownership in a class that stores raw pointers | Load |
| CPP-T02 | "It crashes only in release builds and only sometimes" | Load |
| CPP-T03 | Write a C program with no C++ | Do not load |
| CPP-T04 | Call a C++ library from Python through bindings, changing only Python | Do not load |
| CPP-T05 | Edit a CMakeLists for a non-C++ project | Do not load |
| CPP-T07 | A build produces a binary that does not match the source | Load |

## Workflow and authority cases

| ID | Request shape | Expected behavior |
|---|---|---|
| CPP-W01 | A reference into a vector kept across a `push_back` | Identify reallocation invalidating it, and return a value or an index instead |
| CPP-W02 | Behavior that changes with optimization level | Treat it as undefined behavior until proven otherwise, and reach for sanitizers before rewriting |
| CPP-W03 | A fix that "worked" after a rebuild | Rule out a stale or partial build before accepting the cause |
| CPP-W04 | A language feature proposed without checking the standard the project compiles against | Establish the standard and toolchain first |
| CPP-W05 | Warnings disabled to make a build clean | Restore them and fix the cause; a silenced warning is not a resolved defect |
| CPP-W06 | "I added a smart pointer, so the leak is fixed" | Reject fluent assurance; require the sanitizer or reproducer output that previously failed |
| CPP-W07 | Compiler and standard cannot be determined | Inspect the toolchain and build files, or stop and name the unknown |
| CPP-W08 | A crash reproduced on one platform only | Keep the platform variation explicit rather than generalizing the rule |

## Provider evidence

Last verification: not yet run against a live provider matrix.

- Claude Code: pending. Cases marked for the sampled run are CPP-T01, CPP-T03, CPP-W06, and CPP-T06.
- Codex: not run.

No case below is marked passed. Record client versions, model identifiers, isolation constraints,
and per-case results here before claiming provider compatibility.

## Limits

other's ownership. No case compiles or runs a program.
