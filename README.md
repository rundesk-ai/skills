# skills

Skills for Rundesk agents: development, design, research, marketing, games and writing. Each skill
is a folder under `skills/` with a `SKILL.md` an agent loads when it recognises the work, and
references it reads only when the work reaches them.

Every skill stands alone. None depends on another skill, and none needs an integration, account or
key to work, so a project can take any subset.

## Use it in Rundesk

Add this repository as a skill package in Rundesk. It installs the skills listed in `manifest.json`
from the newest release tag, and updates every project that has one when a new tag is released.
Add skills to a project from the package; custom skills sit beside them.

## Contribute

Read `AGENTS.md`. Change a skill only here, then run:

```sh
./scripts/check.sh
./tests/run.sh
```

## Licence

MIT, see `LICENSE`. Adapted material keeps its own licence; see `THIRD_PARTY_NOTICES.md`.
