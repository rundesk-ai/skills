# Sources

- **AGENTS.md convention** — https://agents.md/ — plain Markdown read by most agent CLIs; nearest
  file in the tree wins; user prompts override.
- **Claude Code memory** — https://code.claude.com/docs/en/memory — Claude Code reads `CLAUDE.md`;
  about 200 lines per file, longer files lower adherence; contradictions are resolved arbitrarily;
  what must always happen belongs in a check or hook.
- **Claude Code best practices** — https://code.claude.com/docs/en/best-practices — cut any line
  whose removal causes no mistake; include what cannot be guessed, exclude what the code shows;
  emphasise one skipped rule, not many; test edits by behaviour.
- **Claude prompting best practices** —
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  — give the reason behind an instruction; say what to do rather than what not to; aggressive
  wording makes current models overtrigger.
- **Effective context engineering for AI agents** —
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — the minimal set
  of information that fully outlines behaviour; load up front only what every task needs.
- **Codex AGENTS.md** — https://developers.openai.com/codex/guides/agents-md — Codex reads
  `AGENTS.md`, root first, with a 32 KiB default cap that drops the most specific files first.
- **How Many Instructions Can LLMs Follow at Once?** — https://arxiv.org/abs/2507.11538 — accuracy
  falls as instruction count rises, with a bias toward earlier instructions.
- **Ponytail** — https://github.com/DietrichGebert/ponytail — the "first option that fully works"
  ladder, "lazy about the solution, never about the change", a never-cut list, a closing line naming
  what was skipped and the risk, and a `shortcut:` comment convention. The smallest-change rule's
  list of every place a change must reach, its list of code not to add (abstraction, wrapper,
  option, config, "for later" code), "deletion beats addition", and "code you move or merge keeps
  its error handling and validation" are adapted from its `AGENTS.md`. MIT licence, Copyright (c)
  2026 DietrichGebert: the above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT
  WARRANTY OF ANY KIND.
- **Orphans left by finished changes** — the "delete what it leaves unused; list anything already
  unused for the owner" clause of step 4 comes from a private multi-project simulation (2026-10)
  whose instructions already carried the full smallest-change rule, yet about two dozen review rounds
  removed helpers, tests, assets and comments whose only caller an earlier change had removed. Its
  review log also held already-unused code for the owner to decide on, which is why the clause lists
  existing dead code rather than deleting it. Measured once on a 1,000-line C# case with four
  sequential agents: arms with and without the clause both scored 9-10 of 10, so the benefit is
  unproven at that size.
