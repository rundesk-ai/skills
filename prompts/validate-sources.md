# Validate a skill's sources

## Skill

> Replace this line with the name of one skill in `skills/`.

Check every claim the skill above makes against the source behind it: that the source exists, that it
is the one closest to the thing, that it still says what the skill attributes to it, and that the
version it describes is the version the skill claims. One skill per run. If the line above still
reads as the instruction to replace it, ask which skill and stop.

A skill is read instead of the source. A claim nobody has traced looks exactly like one that was
checked, and an agent acts on both.

## Before starting

1. Load `researching-topics` and read `references/source-evaluation.md` in full. It owns lateral
   reading, provenance and what makes a source strong for a claim; this prompt adds what to do with
   the result.
2. Read the skill and every file in its `references/` folder. You cannot check claims you have not
   read.
3. Read `references/sources.md` if the skill has one. Sixty-two of the sixty-five skills here do, and
   it is where the answer is recorded.

Opening sources needs the network. A source you could not open is recorded as **unchecked** — never
as verified, and never as broken.

## 1. Inventory the claims

List every claim in the skill and its references, one per line, before opening a single source:

```text
claim | file and heading | the source it rests on, or none
```

A claim is anything an agent would act on: a rule, a default, a number, a limit, a version, a flag, a
file name, an error message, a named trap, or a statement about how something behaves. Prose that
says what to do next is not a claim; prose that says what is true is.

## 2. Check each source

For each source in `references/sources.md`, and for each claim that names one:

- **Open it.** A link that redirects to a section index, a versioned page that moved, or a 404 is a
  finding, not a detail.
- **Find the passage** that establishes the claim. A source that is about the subject but never states
  the claim supports nothing, and that is the most common failure here.
- **Check the scope.** A claim stated for one version, one platform or one configuration, written in
  the skill as though it were general, is wrong for every reader outside that scope.
- **Check it is the closest source.** A specification, the source code, the official documentation or
  the original study beats an article about any of them. A secondary source standing in for a primary
  one available is a finding.
- **Check the version.** Where the skill pins a version, compare it against what the project ships
  now. Where the skill pins none and the behavior is version-bound, that is a finding of its own.
- **Record the date you opened it**, because the next run needs to know what was current when.

## 3. Check the mapping both ways

- **A claim with no source.** Either find one, or the claim is recollection and comes out.
- **A source supporting no claim.** It is paid for on every read of the file and earns nothing. Cut
  it, or say which claim it is there for.
- **A source that says less than the claim.** Narrow the claim to what the source states. Never
  soften it into a hedge — "generally", "typically" and "in most cases" are how an unverified claim
  survives review.
- **Repeated reporting counted as confirmation.** Three pages tracing to one announcement are one
  source.

## 4. Check what the skill may name

`./scripts/check.sh` refuses an absolute path and a reference to another skill. It does not catch a
link out of the skill's own directory, and twenty skills here link
`../../../docs/guides/validation.md`, which this repository does not have. Check for all four:

- no absolute path, and no link that leaves the skill's own directory;
- no repository, project, company or machine named as though every reader has it;
- no other skill named, because the project receiving this one may not take that one;
- every link inside the skill resolves to a file the skill ships.

## 5. Record it

Update `references/sources.md` in place: correct entries, remove dead ones, and end the file with a
single line saying when it was last checked and against what. Leave a source you could not open in
the file, marked unchecked, with the date you tried.

**Do not rewrite the skill's claims in the same run.** Report them and let the change be decided;
a claim edited by whoever found it loses the second reading that catches a wrong correction.

## Report

Ranked, most serious first, each with the file, the line and the source:

1. **False** — the source contradicts the claim.
2. **Stale** — the source has moved on, or the version the claim describes is no longer the one that
   ships.
3. **Dead** — the source cannot be reached, and no replacement was found.
4. **Unsupported** — the claim has no source, or its source never states it.
5. **Weak** — a secondary source standing in for a primary one that exists.
6. **Unused** — a source no claim rests on.
7. **Portability** — a path, a repository, a machine or another skill named in the skill.

Then: how many claims were checked, how many were verified, how many are unchecked and why.

Do not commit or push unless you were asked to.
