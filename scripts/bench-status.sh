#!/usr/bin/env bash
# Say which skills a benchmark run is due for, so a skill measured recently is not measured again.
#
#   scripts/bench-status.sh [skill...]           every skill, or the named ones
#   scripts/bench-status.sh --due [skill...]     only the skills a run is due for
#   scripts/bench-status.sh --hash <skill>       the fingerprint to record as "skill_hash"
#
#   --max-age DAYS   a result older than this is due again (default 90): agents and models move
#
# A skill is current when its newest result under bench/results/<skill>/ measured exactly what is
# there now: the skill's files and its bench/<skill>/cases and fixtures. A result records that as
# "skill_hash"; an older result without one is compared against the commit that added it.
#
# Statuses: current, changed (the skill, cases or fixtures moved since), old (past --max-age),
# never (no result), unknown (no hash and no commit to compare against).
# Exits 0 when every skill listed is current, 1 when any is due, 2 on a usage error.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

exec python3 - "$@" <<'PY'
import datetime, hashlib, json, os, subprocess, sys

def usage(msg):
    print(f"{msg}\nusage: scripts/bench-status.sh [--due] [--max-age DAYS] [skill...] | --hash <skill>", file=sys.stderr)
    sys.exit(2)

def skill_dirs():
    found = {}
    for g in sorted(os.listdir("skills")):
        gd = os.path.join("skills", g)
        if not os.path.isdir(gd):
            continue
        for n in sorted(os.listdir(gd)):
            if os.path.isfile(os.path.join(gd, n, "SKILL.md")):
                found[n] = os.path.join(gd, n)
    return found

def measured_paths(name, path):
    # Labelled by role, not location, so moving a skill between groups does not make it due.
    return {"skill": path, "cases": os.path.join("bench", name, "cases"),
            "fixtures": os.path.join("bench", name, "fixtures")}

def fingerprint(files):
    # Sorted (relative path, content) pairs, so the same files give the same hash anywhere.
    digest = hashlib.sha256()
    for rel, content in sorted(files):
        digest.update(rel.encode() + b"\0" + content + b"\0")
    return digest.hexdigest()[:16]

def working_files(paths):
    files = []
    for label, top in paths.items():
        for dirpath, dirnames, filenames in os.walk(top):
            # Bytecode a test run leaves behind is not part of what was measured.
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in filenames:
                fp = os.path.join(dirpath, fn)
                with open(fp, "rb") as f:
                    files.append((label + "/" + os.path.relpath(fp, top), f.read()))
    return files

def git(*args):
    r = subprocess.run(["git", *args], capture_output=True)
    return r.returncode, r.stdout

def committed_files(commit, name, paths):
    # The skill may have sat elsewhere then; find it by name, as a group move keeps the name.
    code, out = git("ls-tree", "-r", "--name-only", commit)
    if code != 0:
        return None
    tree = out.decode().splitlines()
    marker = [t[: -len("/SKILL.md")] for t in tree
              if t.startswith("skills/") and t.endswith(f"/{name}/SKILL.md") and "/variants/" not in t]
    roots = dict(paths, skill=marker[0] if marker else paths["skill"])
    files = []
    for label, top in roots.items():
        for t in tree:
            if t.startswith(top + "/") and "/__pycache__/" not in t:
                _, content = git("show", f"{commit}:{t}")
                files.append((label + "/" + t[len(top) + 1:], content))
    return files

def changed_since_commit(name, result_file, paths):
    code, out = git("log", "--diff-filter=A", "--format=%H", "-1", "--", result_file)
    commit = out.decode().strip()
    if code != 0 or not commit:
        return None
    then = committed_files(commit, name, paths)
    return then is None or fingerprint(then) != fingerprint(working_files(paths))

def status(name, path, max_age, today):
    results = os.path.join("bench", "results", name)
    files = sorted(f for f in os.listdir(results) if f.endswith(".json")) if os.path.isdir(results) else []
    if not files:
        return "never", "-", "no result recorded"
    newest = os.path.join(results, files[-1])
    with open(newest, encoding="utf-8") as f:
        result = json.load(f)
    date = result.get("date") or files[-1][:-5]
    paths = measured_paths(name, path)
    if result.get("skill_hash"):
        changed = result["skill_hash"] != fingerprint(working_files(paths))
        basis = "skill_hash"
    else:
        changed = changed_since_commit(name, newest, paths)
        basis = "the commit that added the result"
        if changed is None:
            return "unknown", date, "no skill_hash, and the result is not committed"
    if changed:
        return "changed", date, f"skill, cases or fixtures differ from {basis}"
    age = (today - datetime.date.fromisoformat(date)).days
    if age > max_age:
        return "old", date, f"{age} days old, past --max-age {max_age}"
    return "current", date, f"{age} days old, unchanged"

args = sys.argv[1:]
due_only, max_age, names = False, 90, []
while args:
    a = args.pop(0)
    if a == "--due":
        due_only = True
    elif a == "--max-age":
        if not args or not args[0].isdigit():
            usage("--max-age needs a number of days")
        max_age = int(args.pop(0))
    elif a == "--hash":
        if len(args) != 1:
            usage("--hash takes one skill")
        names = args
        break
    elif a in ("-h", "--help"):
        usage("")
    else:
        names.append(a)

dirs = skill_dirs()
for n in names:
    if n not in dirs:
        usage(f"no such skill: {n}")

if "--hash" in sys.argv[1:]:
    print(fingerprint(working_files(measured_paths(names[0], dirs[names[0]]))))
    sys.exit(0)

today = datetime.date.today()
due = False
for n in names or sorted(dirs):
    s, date, detail = status(n, dirs[n], max_age, today)
    due = due or s != "current"
    if not due_only or s != "current":
        print(f"{n:34} {s:8} {date:10}  {detail}")
sys.exit(1 if due else 0)
PY
