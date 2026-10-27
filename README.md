# skills

Skills for any coding agent, in eight groups under `skills/`: development, writing, design,
research, marketing, stacks, games and media. Each skill is a folder with a `SKILL.md` an agent loads when
it recognises the work, and references it reads only when the work reaches them.

Every skill stands alone. None depends on another skill, and none needs an integration, account or
key to work, so a project can take any subset.

## Use them

Copy any skill folder into the folder your agent reads skills from, such as `.agents/skills/` or
`.claude/skills/`. Take the newest release tag rather than `main`.

`manifest.json` lists every skill by name and path, in the format the Rundesk app and the Rundesk
CLI read: add this repository as a skill package and they install the skills from the newest
release tag, and update every project that has one when a new tag is released.

`subagents/` holds review subagents, listed under `subagents` in the same manifest. A Rundesk app
that reads them writes each into every agent CLI on the machine while its subagents setting is on.

## Contribute

Read `AGENTS.md`. Change a skill only here, then run:

```sh
./scripts/check.sh
./tests/run.sh
```

## Licence

MIT, see `LICENSE`. Adapted material keeps its own licence; see `THIRD_PARTY_NOTICES.md`.
