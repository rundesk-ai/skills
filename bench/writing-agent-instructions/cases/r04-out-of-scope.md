+++
skill = "writing-agent-instructions"
cases_version = 1
kind = "routing"
expect = "no-fire"
fixture = "tally"
rubric = "Writes a skill's own instructions without loading this skill, which declines that work."
+++
Write a skill, as a SKILL.md with its frontmatter, that teaches an agent how the maintainer cuts a
release of this package. Put it in `release-skill/SKILL.md`.
