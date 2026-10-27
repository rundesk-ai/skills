#!/usr/bin/env bash
# Validate the catalog itself. Runs anywhere — it never needs a target repository.
#
#   scripts/check.sh
#
# Refuses: a skill outside a group (skills/<group>/<name>/), a name used in two groups, a skill
# directory without SKILL.md, frontmatter that never closes, one whose name does not match
# its directory or does not start with its group's prefix, a missing or stub description or one not
# starting "Use when" (or "Use before"), a reference no link reaches, a sentence cut off mid-way, a
# variant that overlays nothing or removes a file the base does not have, a rules file that has
# drifted from its copy, a manifest that does not list exactly the skills and subagents in the tree,
# a subagent whose name does not match its file or whose description does not start "Use when",
# a frontmatter value a YAML parser would reject or cut short (an unquoted ": " or " #"),
# and the three things that stop a skill standing alone — an absolute path, a reference to
# another skill, and a dependency on an integration's tools.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail=0

echo "== AGENTS.md / CLAUDE.md"
# CLAUDE.md is AGENTS.md with only the first heading's AGENTS changed to CLAUDE.
if cmp -s <(sed '1s/AGENTS/CLAUDE/' AGENTS.md) CLAUDE.md; then
  echo "  ok  CLAUDE.md mirrors AGENTS.md"
else
  echo "  !!  AGENTS.md and CLAUDE.md differ — regenerate: sed '1s/AGENTS/CLAUDE/' AGENTS.md > CLAUDE.md"
  fail=1
fi

echo "== shell scripts"
for f in scripts/*.sh; do
  if bash -n "$f" 2>/dev/null; then
    echo "  ok  $f"
  else
    echo "  !!  $f has a syntax error"; bash -n "$f" || true
    fail=1
  fi
done

echo "== skills"
python3 - <<'PY' || fail=1
import os, re, sys, urllib.parse

ABSOLUTE = re.compile(r"(?:^|[\s`(\[])(?:/Users/|/home/|[A-Za-z]:\\\\)")


def plain_scalar_fault(val):
    """Say why a YAML parser would misread an unquoted frontmatter value, or return None.

    Installers parse frontmatter as YAML and reject the whole package when one file fails, so a
    value this hand-rolled reader accepts must also be one a real parser accepts.
    """
    val = val.strip()
    if not val or val[0] in "'\"|>":
        return None
    if ": " in val or val.endswith(":"):
        return "an unquoted ': ', which YAML reads as a nested mapping"
    if " #" in val:
        return "an unquoted ' #', which YAML reads as the start of a comment"
    if val[0] in "[{&*!%@`,#?-" and not (val[0] in "?-" and val[1:2] not in (" ", "")):
        return f"an unquoted leading {val[0]!r}, which YAML reads as syntax, not text"
    return None


problems = []
names = []
# Skills sit one level down, in a group: skills/<group>/<name>/. The group only organizes this
# repository; every project gets skills flat by name, so a name is unique across all groups.
dirs = {}
for g in sorted(os.listdir("skills")):
    gd = os.path.join("skills", g)
    if not os.path.isdir(gd):
        continue
    if os.path.isfile(os.path.join(gd, "SKILL.md")):
        problems.append(f"{gd}: a skill directly under skills/ — put it in a group, skills/<group>/{g}/")
        continue
    for n in sorted(os.listdir(gd)):
        d = os.path.join(gd, n)
        if not os.path.isdir(d):
            continue
        if not os.path.isfile(os.path.join(d, "SKILL.md")):
            problems.append(f"{d}: no SKILL.md (a directory is a skill iff it has one)")
            continue
        if n in dirs:
            problems.append(f"{d}: the name {n!r} is already used by {dirs[n]} — names are unique across groups")
            continue
        dirs[n] = d
for n in sorted(dirs):
    d = dirs[n]
    skill = os.path.join(d, "SKILL.md")
    names.append(n)

    with open(skill, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---\n"):
        problems.append(f"{n}: SKILL.md has no YAML frontmatter")
        continue
    # The closing fence must be alone on its line. Glued to the end of the description
    # -- "...do not use for X.---" -- the block never closes, and a parser stricter than
    # the one that wrote it reads the whole skill as frontmatter, or none of it.
    head, sep, _ = text[4:].partition("\n---\n")
    if not sep:
        problems.append(f"{n}: the frontmatter does not close with --- alone on a line")
        continue
    fm = head
    got = {}
    key = None
    for line in fm.split("\n"):
        if line[:1] not in (" ", "\t", "") and ":" in line:
            key, _, val = line.partition(":")
            got[key.strip()] = val.strip()
        elif key and line.strip():
            got[key] = got.get(key, "") + " " + line.strip()

    for key, val in got.items():
        fault = plain_scalar_fault(val)
        if fault:
            problems.append(f"{n}: frontmatter {key} has {fault}; installers reject the whole package — reword it")
    if got.get("name") != n:
        problems.append(f"{n}: frontmatter name is {got.get('name')!r}, expected {n!r}")
    desc = got.get("description", "").strip()
    if len(desc) < 40:
        problems.append(f"{n}: description is missing or too short to trigger on")
    # "Use before" is the form for a skill linked to an integration: it must load before any call.
    elif not desc.strip("'\"").startswith(("Use when", "Use before")):
        problems.append(f"{n}: description must start 'Use when' — it is the whole trigger, read before the skill loads")

    # variants
    vdir = os.path.join(d, "variants")
    if os.path.isdir(vdir):
        for v in sorted(os.listdir(vdir)):
            vp = os.path.join(vdir, v)
            if not os.path.isdir(vp):
                continue
            remove = os.path.join(vp, ".remove")
            if os.path.isfile(remove):
                with open(remove, encoding="utf-8") as f:
                    removals = [ln.strip() for ln in f]
                for rel in removals:
                    if not rel or rel.startswith("#"):
                        continue
                    if not os.path.exists(os.path.join(d, rel)):
                        problems.append(
                            f"{n}@{v}: .remove names {rel}, which the base does not have")
            files = [f for f in os.listdir(vp) if f != ".remove"]
            if not files:
                problems.append(f"{n}@{v}: variant overlays nothing")

FENCE = re.compile(r"(`{3,}|~{3,})")
HEADING = re.compile(r"#{1,6}\s")


def prose(lines):
    """(index, line) for each line outside a fenced block; a fence closes only on its own marker."""
    marker = None
    for i, line in enumerate(lines):
        opened = FENCE.match(line.lstrip())
        if marker is None and opened:
            marker = opened.group(1)
        elif marker is not None and opened and opened.group(1)[0] == marker[0] and len(opened.group(1)) >= len(marker):
            marker = None
        elif marker is None:
            yield i, line


# Every reference is reachable from SKILL.md through links: one nothing points at is never read, and
# is usually a test record or a leftover that should not ship. Only links inside the skill count.
INLINE = re.compile(r"\]\(\s*<?([^)\s>#]+)>?(?:#[^)\s]*)?(?:\s+[\"'(][^)]*)?\)")
DEFINED = re.compile(r"^\s*\[[^\]]+\]:\s*<?([^\s>#]+)")
for n in names:
    d = os.path.realpath(dirs[n])
    refs = os.path.join(d, "references")
    if not os.path.isdir(refs):
        continue
    seen, todo = set(), [os.path.join(d, "SKILL.md")]
    while todo:
        fp = os.path.realpath(todo.pop())
        if fp in seen or not os.path.isfile(fp) or not fp.startswith(d + os.sep):
            continue
        seen.add(fp)
        if fp.endswith(".md"):
            with open(fp, encoding="utf-8", errors="replace") as f:
                for _, line in prose(f.read().splitlines()):
                    for target in INLINE.findall(line) + DEFINED.findall(line):
                        todo.append(os.path.join(os.path.dirname(fp), urllib.parse.unquote(target)))
    for dirpath, _, filenames in os.walk(refs):
        for fn in filenames:
            fp = os.path.realpath(os.path.join(dirpath, fn))
            if fp not in seen and not fn.startswith("."):
                problems.append(f"{os.path.relpath(fp)}: no link reaches it from SKILL.md — link it with when to read it, or remove it")

# A line ending on a dangling word before a break is a sentence cut short — what removing a sibling's
# name from the middle of a sentence leaves behind.
DANGLING = re.compile(r"\b(to|with|and|or|Use|the|of|for|an|by|from|into|than|under)$|[;,]$")
for n in names:
    for dirpath, _, filenames in os.walk(dirs[n]):
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
            for i, line in prose(lines):
                bare = line.lstrip()
                if not bare or bare.startswith(("|", ">")) or HEADING.match(bare):
                    continue
                after = lines[i + 1].lstrip() if i + 1 < len(lines) else ""
                breaks = not after or after.startswith("|") or HEADING.match(after) or FENCE.match(after)
                if DANGLING.search(line.rstrip()) and breaks:
                    problems.append(f"{fp}:{i + 1}: sentence ends mid-way — finish it or cut it")

# Each group has the prefixes its names start with, listed once in skills/groups.txt, so a name
# says which group it belongs to and one kind of work keeps one prefix.
prefixes = {}
try:
    with open(os.path.join("skills", "groups.txt"), encoding="utf-8") as f:
        for line in f:
            parts = line.split("#", 1)[0].split()
            if parts:
                prefixes[parts[0]] = tuple(parts[1:])
except OSError:
    problems.append("skills/groups.txt: missing — it lists each group and its name prefixes")
for n in names:
    group = os.path.basename(os.path.dirname(dirs[n]))
    if group not in prefixes:
        problems.append(f"{dirs[n]}: the group {group!r} is not listed in skills/groups.txt")
    elif not n.startswith(prefixes[group]):
        problems.append(f"{n}: a name in {group} starts with {' or '.join(prefixes[group])} (skills/groups.txt)")

# A skill is read wherever it lands, so it may name no machine and no sibling.
name_pat = re.compile(r"\b(" + "|".join(re.escape(n) for n in names) + r")\b")
for n in names:
    d = dirs[n]
    for dirpath, _, filenames in os.walk(d):
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    if ABSOLUTE.search(line):
                        problems.append(f"{fp}:{i}: absolute path — a skill runs anywhere")
                    # a URL may contain a skill's words (".../a-lesson-in-game-design-for...")
                    for m in name_pat.findall(re.sub(r"https?://\S+", "", line)):
                        if m != n:
                            problems.append(
                                f"{fp}:{i}: names the skill {m!r} — each skill stands alone")

# A skill stands alone: it may not need an integration to work, so it names no MCP tool. A tool it
# can use when present is described by what it does, never by the name only that setup gives it.
TOOL = re.compile(r"\bmcp__[A-Za-z0-9_-]+")
for n in names:
    for dirpath, _, filenames in os.walk(dirs[n]):
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    if TOOL.search(line):
                        problems.append(f"{fp}:{i}: names an integration's tool — a skill needs no integration to work")

# A subagent is one file, subagents/<name>.md, in the format the Rundesk subagent library stores. It is
# copied into every agent CLI on the machine, so it stands alone as a skill does.
subagents = {}
if os.path.isdir("subagents"):
    for fn in sorted(os.listdir("subagents")):
        fp = os.path.join("subagents", fn)
        if not fn.endswith(".md") or not os.path.isfile(fp):
            problems.append(f"{fp}: subagents/ holds only <name>.md files")
            continue
        n = fn[:-3]
        subagents[n] = fp
        with open(fp, encoding="utf-8") as f:
            text = f.read()
        head, sep, _ = text[4:].partition("\n---\n") if text.startswith("---\n") else ("", "", "")
        if not sep:
            problems.append(f"{fp}: the frontmatter does not close with --- alone on a line")
            continue
        top = {}
        for line in head.split("\n"):
            if line[:1] not in (" ", "\t", "-", "") and ":" in line:
                key, _, val = line.partition(":")
                fault = plain_scalar_fault(val)
                if fault:
                    problems.append(f"{fp}: frontmatter {key.strip()} has {fault}; installers reject the whole package — reword it")
                top[key.strip()] = val.strip().strip("'\"")
        if top.get("name") != n:
            problems.append(f"{fp}: frontmatter name is {top.get('name')!r}, expected {n!r}")
        desc = top.get("description", "")
        if len(desc) < 40 or not desc.startswith("Use when"):
            problems.append(f"{fp}: description must start 'Use when' and say when to delegate to it")
        for i, line in enumerate(text.splitlines(), 1):
            if ABSOLUTE.search(line):
                problems.append(f"{fp}:{i}: absolute path — a subagent runs anywhere")
            if TOOL.search(line):
                problems.append(f"{fp}:{i}: names an integration's tool — a subagent needs no integration to work")
            for m in name_pat.findall(re.sub(r"https?://\S+", "", line)):
                problems.append(f"{fp}:{i}: names the skill {m!r} — a subagent stands alone")

# manifest.json lists exactly the skills in the tree, by name and path, so a package install gets them all.
import json
try:
    with open("manifest.json", encoding="utf-8") as f:
        manifest = json.load(f)
except (OSError, ValueError) as e:
    problems.append(f"manifest.json: cannot be read ({e})")
    manifest = None
if manifest is not None:
    for key in ("schema", "name", "version", "description", "skills"):
        if key not in manifest:
            problems.append(f"manifest.json: missing {key!r}")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
        problems.append("manifest.json: version must be MAJOR.MINOR.PATCH")
    listed = manifest.get("skills") or []
    got_names = [s.get("name") for s in listed]
    for s in listed:
        if s.get("name") in dirs and s.get("path") != dirs[s.get("name")]:
            problems.append(f"manifest.json: {s.get('name')!r} has path {s.get('path')!r}, expected {dirs[s.get('name')]}")
    for m in sorted(set(names) - set(got_names)):
        problems.append(f"manifest.json: does not list the skill {m!r}")
    for m in sorted(set(got_names) - set(names)):
        problems.append(f"manifest.json: lists {m!r}, which is not a skill in the tree")
    if got_names != sorted(got_names) or len(got_names) != len(set(got_names)):
        problems.append("manifest.json: skills must be listed once each, sorted by name")
    # subagents is optional, and lists exactly the files in subagents/ the same way.
    listed = manifest.get("subagents") or []
    got_names = [s.get("name") for s in listed]
    for s in listed:
        if s.get("name") in subagents and s.get("path") != subagents[s.get("name")]:
            problems.append(f"manifest.json: subagent {s.get('name')!r} has path {s.get('path')!r}, expected {subagents[s.get('name')]}")
    for m in sorted(set(subagents) - set(got_names)):
        problems.append(f"manifest.json: does not list the subagent {m!r}")
    for m in sorted(set(got_names) - set(subagents)):
        problems.append(f"manifest.json: lists {m!r}, which is not a subagent in subagents/")
    if got_names != sorted(got_names) or len(got_names) != len(set(got_names)):
        problems.append("manifest.json: subagents must be listed once each, sorted by name")

# The catalog is public: nothing in a skill, a benchmark or a prompt may carry a credential or a real
# address. Examples use reserved names (example.com, .example, .test) so a pasted secret or a real
# inbox stands out here before it is published.
SECRET = re.compile(r"sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|xox[abpr]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY|AIza[0-9A-Za-z_-]{35}")
EMAIL = re.compile(r"(?<![/\w.%+-])[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}")
RESERVED = re.compile(r"(^|\.)(example\.(com|org|net)|example|test|invalid|localhost)$", re.I)
for top in ("skills", "subagents", "bench", "prompts"):
    for dirpath, _, filenames in os.walk(top):
        for fn in filenames:
            if not fn.endswith((".md", ".json", ".toml", ".py", ".txt", ".yml", ".yaml")):
                continue
            fp = os.path.join(dirpath, fn)
            with open(fp, encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    if SECRET.search(line):
                        problems.append(f"{fp}:{i}: looks like a credential — never publish one")
                    for m in EMAIL.finditer(line):
                        domain = m.group(0).split("@", 1)[1]
                        if not domain.lower().endswith((".html", ".htm")) and not RESERVED.search(domain) and not m.group(0).lower().startswith("noreply@"):
                            problems.append(f"{fp}:{i}: real email address {m.group(0)!r} — use a reserved domain such as example.com")

print(f"  {len(names)} skills, {len(subagents)} subagents")

for p in problems:
    print(f"  !!  {p}")
sys.exit(1 if problems else 0)
PY

echo
if [ "$fail" -ne 0 ]; then
  echo "catalog check failed"
  exit 1
fi
echo "catalog is sound"
