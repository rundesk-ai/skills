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
  what was skipped and the risk, and a `shortcut:` comment convention.
