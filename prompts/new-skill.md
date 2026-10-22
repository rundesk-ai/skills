# Research and write a new skill

## Subject

> Replace this line with the work the skill would cover, in the words someone asking for it would
> use.

Add one skill to the catalog for the subject above: research the practice first, prove no existing
skill owns it, write it to the authoring contract, place it in a family, and prove it fires and
helps. Everything below is about that subject and nothing else. Stop and report instead of guessing
wherever this prompt says to, starting here — if the subject still reads as the line telling you to
replace it, ask what it is and stop.

## Before starting

1. Load `writing-skills` and read `SKILL.md` and, in its references folder, `descriptions.md` and
   `evaluating.md` in full. They are the contract; this prompt only adds what is specific to working
   here.
2. Read `AGENTS.md`. A skill names no repository, no path, no machine and no other skill —
   `./scripts/check.sh` refuses all four.
3. Run `./scripts/deploy.sh --list` and read every description. You cannot prove a skill is missing
   without them.
4. Read two skills from the family the subject would land in, in full, as models for depth and voice.

## 1. Prove the skill does not exist

`writing-skills` says extend before you create. Do that test here with evidence, because the catalog
has already lost skills to it:

- Match the subject against every description, then read the body of every plausible match.
- Compare the reference filenames the subject would need against those each candidate already has. Two
  skills sharing most of their filenames are one skill with two names — that is how `cpp-patterns`
  and `using-cpp` became copies nothing compared.
- **Extend the owner** when the new capability shares its trigger, its workflow and its judgment.
  Add a section or a reference there and stop; the report says which skill you extended and why.
- **Write a variant** when only the wording differs by stack: `skills/<name>/variants/<variant>/`
  holding only the files that change, and `.remove` for base files it drops.
- **Create a skill** only when the trigger is genuinely different. Write that difference down in one
  sentence; a name that sounds adjacent is not a reason.

## 2. Research the practice

The deliverable of this step is not a briefing. It is a **practice**: the steps in execution order,
the one strong default at each step, the traps as symptom, cause, replacement and proof, and the
evidence behind each. Load `researching-topics` for the search and evidence workflow, and use these
sources in this order.

**Primary material first**: the specification, the source, the official documentation for the exact
version, the original study. **Then practitioner evidence**: maintainer discussions, postmortems,
issue threads — that is where the traps live, and the formal contract rarely names them.

Record every source in the skill's `references/sources.md` as you go, with what each one established.
A source found after the prose is written is a citation chosen to fit.

## 3. Write the description first

It is the only part in context before the skill fires, an agent pays for it on every turn, and the
body is unreachable until routing succeeds. Write all three clauses, in this order:

```yaml
description: Use when <the work, as a person would describe it, including the indirect requests that
  never name the skill>. It supplies <the judgment and procedure the agent gets>. Do not use <the
  near miss that would otherwise steal the trigger>.
```

- **All three clauses, every time.** The catalog's own pages mark a missing purpose or boundary in
  red, and a reader cannot tell an absent clause from a skill that declines nothing.
- **Budget: about 135 tokens.** The 65 skills here run 87 to 179, and every one of them is loaded in
  every session whether or not it fires.
- Route on intent, not on implementation. Name a tool or file type only where it decides whether the
  skill should fire.
- Lean toward firing. A skill that loads and proves unneeded costs one read; a skill that stays
  silent costs the whole task.

## 4. Write the skill

- **Budget: about 1,800 tokens of body**, and about 8,600 with its references. The largest skill here
  is 4,100 tokens of body, and past that you are writing a reference, not a skill.
- `SKILL.md` holds the core procedure, one strong default and the non-obvious traps. Conditional
  depth goes to `references/`, introduced by a line saying when to read it.
- Explain why a rule exists. An agent given the reason applies it to the case you did not foresee.
- Write no README, no changelog and no record of how the skill came to be.

## 5. Place it in the catalog

Name it `<verb>-<object>` with a verb from the Name the work table in `writing-skills`; `check.sh`
refuses any other. A directory under `skills/` that holds `SKILL.md` is a skill; nothing else lists it. Once the gates
pass, it is committed and merged, and it ships with the next release of this catalog; Rundesk
installs the catalog as a package and updates every project that has the skill. Never create it in
Rundesk's library first.

## 6. Prove it

1. **Test the trigger** in fresh sessions: a direct request, an indirect request that never names the
   skill, and a near miss that must not load it. Fix routing by category, never by pasting the
   failing phrase into the description.
2. **Compare against no skill** on two or three realistic tasks, reading the outputs and the
   transcripts rather than the summaries.
3. **Benchmark it across the installed agents** with `prompts/benchmark-skill.md`. A description
   that fires on one agent does not always fire on another.

## 7. Gates

```sh
./scripts/check.sh              # the catalog: naming, frontmatter, portability
./tests/run.sh                  # the deploy and check tests
```

## Refusals

Stop and report rather than proceed when: the subject is already covered by a skill; the research turns
up no evidence beyond recollection; the subject only makes sense inside one repository, one company or
one deployment; or the skill cannot be written without naming another skill.

## Report

1. One line: the subject, the decision — extended, variant or new — and the reason.
2. What the research library held, what it did not, and every page cited by library path.
3. The description, with the three clauses marked, and its token count.
4. The skill's shape: body tokens, each reference and what it holds, total tokens.
5. The trigger tests: the three requests and what each one did.
6. The comparison against no skill: what differed, and which part of the skill did it.
7. The gates, and their output.
8. What is still unproven.

Do not commit or push unless you were asked to.
