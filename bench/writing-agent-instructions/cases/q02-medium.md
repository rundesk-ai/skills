+++
skill = "writing-agent-instructions"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "pantry"
rubric = """
result.1  `AGENTS.md` and `CLAUDE.md` both exist and are byte-identical, and the file says they are a pair changed together.
result.2  Something checks the pair: a test or check that fails when the two files differ, wired into a command the file names.
result.3  The sections follow a task from start to finish: what the repository is, what to do before working, the hard rules, the commands, and a definition of done as the last section.
result.4  Every command listed as a gate leaves the tree unchanged: `make check` and `make fmt` rewrite files through `tools/fmt.py --write`, so the file gives `python3 tools/fmt.py --check pantry tests` and `make test` (or says plainly that `make check` rewrites files); `make release` is not offered as a routine command.
result.5  It carries one smallest-complete-change rule with both halves: add nothing unasked (no abstraction, wrapper, option or "for later" code) and touch nothing outside the task; and finish the change (callers, tests, docs) and remove what it leaves unused.
result.6  That rule, or the hard rules, name this repository's own guards rather than generic ones: at least two of — SQL only in `pantry/store.py`; escaping in `pantry/render.py`; `store.use` refusing to go below zero; shipped migrations never edited.
result.7  The handlers-never-touch-SQLite boundary is stated truthfully: written for new code with `pantry/handlers/export.py` named as the existing exception, or the rule dropped; it is not stated as a fact the code already satisfies.
result.8  Ask-first gates fit this repository: the stored data and its schema (`data/pantry.db`, `migrations/`), dependencies (it has none), and commits; each never-rule carries its reason.
result.9  The file is 250 lines or fewer and holds no file-by-file tour, no language or framework basics, and no count that will go stale.
result.10 Every path and command the file names exists in the repository, and it names no skill that is not in the repository's skills folder.
result.11 The definition of done is numbered, names the gates, asks for observed results, and ends with reporting what was skipped or not checked.
conduct.1 The reply tells the owner what the code already breaks (`pantry/handlers/export.py` opens SQLite itself; `tools/fmt.py --check` fails on the tree today, or `make check` rewrites files).
conduct.2 The reply says what it did not verify and leaves no stray file behind (no `data/`, no scratch file, no rewritten source file).
"""
+++
Set this repo up for coding agents. We use Claude Code and Codex on it.
