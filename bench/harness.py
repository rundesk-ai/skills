"""Benchmark a review subagent: no agent against two versions of it, graded blind.

    python3 -I bench/harness.py run   SUBJECT OUT [--old REF] [--runs N] [--jobs N] [--cases a,b,...]
    python3 -I bench/harness.py judge SUBJECT OUT [--jobs N]
    python3 -I bench/harness.py score SUBJECT OUT

SUBJECT names subagents/SUBJECT.md and its cases in bench/SUBJECT/cases. A case's fixture is a
folder in bench/SUBJECT/fixtures, or "other-subject/name" to reuse one from another subject.

OUT is a new scratch directory outside any git checkout: every run reviews a fresh copy of its
fixture there. The arms are "none" (the case's brief to a plain session), "old" (the agent at git
REF, default the newest tag) and "new" (the agent in the working tree). Each review is graded by a
judge that sees the case's answer key and the review under a random id, never the arm. Findings the
judge marks "unsure" are ruled by a person in OUT/overrides.json ("<id>:<index>": "real", "false"
or "neutral") before scoring; score refuses to run while any is unruled.
"""

import argparse
import concurrent.futures
import itertools
import json
import os
import random
import re
import shutil
import statistics as st
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCH = os.path.join(ROOT, "bench")
SUBJECT = HERE = AGENT = ""  # set by main() from the command line
ARMS = ("none", "old", "new")
REVIEW_MODEL = "claude-sonnet-5-5"  # the model the agent's claude settings name
JUDGE_MODEL = "claude-opus-5-5"
REVIEW_TIMEOUT, JUDGE_TIMEOUT = 1500, 900


def cases(only=None):
    names = sorted(f[:-3] for f in os.listdir(os.path.join(HERE, "cases")) if f.endswith(".md"))
    return [n for n in names if not only or n in only]


def read_case(name):
    text = open(os.path.join(HERE, "cases", name + ".md")).read()
    front, brief = re.match(r"\+\+\+\n(.*?)\n\+\+\+\n(.*)", text, re.S).groups()
    fixture = re.search(r'^fixture = "(.*)"', front, re.M).group(1)
    key = re.search(r'^key = """\n(.*?)^"""', front, re.S | re.M).group(1)
    return fixture, key, brief.strip()


def fixture_dir(fixture):
    owner, _, name = fixture.rpartition("/")
    return os.path.join(BENCH, owner or SUBJECT, "fixtures", name)


def agent_json(text, path):
    _, front, body = text.split("---\n", 2)
    desc = re.search(r'^description: "?(.*?)"?$', front, re.M).group(1)
    json.dump({SUBJECT: {"description": desc, "prompt": body.strip()}}, open(path, "w"))


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, check=True).stdout


def refuse_checkout(out):
    probe = subprocess.run(["git", "-C", out, "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True)
    if probe.stdout.strip() == "true":
        sys.exit(f"{out} is inside a git checkout; reviewers would read its history. Use a scratch directory.")


def review(out, case, arm, n):
    fixture, _, brief = read_case(case)
    run = os.path.join(out, "runs", f"{case}-{arm}-{n}")
    # copytree refuses an existing folder, so a rerun needs a new OUT rather than deleting an old one.
    shutil.copytree(fixture_dir(fixture), run, ignore=shutil.ignore_patterns("__pycache__"))
    cmd = ["claude", "-p", brief, "--model", REVIEW_MODEL, "--restricted", "--strict-mcp-config",
           "--tools", "Read,Grep,Glob,Bash",
           "--allowedTools", "Read,Grep,Glob,Bash(python3 -m unittest:*),Bash(npm test:*),Bash(node --test:*),"
                             "Bash(go test:*),Bash(php tests/run.php:*)",
           "--output-format", "stream-json", "--verbose"]
    if arm != "none":
        cmd += ["--agents", os.path.join(out, "agents", arm + ".json"), "--agent", SUBJECT]
    # Go writes its caches under the home directory and may fetch a toolchain; keep both in OUT.
    env = dict(os.environ, GOCACHE=os.path.join(out, "go", "cache"), GOMODCACHE=os.path.join(out, "go", "mod"),
               GOTOOLCHAIN="local")
    try:
        proc = subprocess.run(cmd, cwd=run, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              timeout=REVIEW_TIMEOUT)
        lines = proc.stdout.splitlines()
    except subprocess.TimeoutExpired:
        lines = []
    result = None
    for line in lines:
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "result":
            result = event
    record = {"case": case, "arm": arm, "n": n, "review": (result or {}).get("result", ""), "ok": bool(result)}
    if result:
        u = result["usage"]
        record.update(tokens=u["input_tokens"] + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u["output_tokens"],
                      cost=result.get("total_cost_usd"), seconds=result.get("duration_ms", 0) / 1000)
    json.dump(record, open(run + ".json", "w"), indent=1)
    return f"{case} {arm} {n}: {'ok' if result else 'FAILED'}"


def cmd_run(a):
    out = os.path.abspath(a.out)
    os.makedirs(out)  # must be new: a run never reuses or clears an earlier one
    os.makedirs(os.path.join(out, "agents"))
    refuse_checkout(out)
    old = a.old or git("describe", "--tags", "--abbrev=0").strip()
    agent_json(git("show", f"{old}:{AGENT}"), os.path.join(out, "agents", "old.json"))
    agent_json(open(os.path.join(ROOT, AGENT)).read(), os.path.join(out, "agents", "new.json"))
    json.dump({"subject": SUBJECT, "old": old, "new": "working tree", "head": git("rev-parse", "HEAD").strip(),
               "claude": subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()},
              open(os.path.join(out, "meta.json"), "w"), indent=1)
    jobs = []
    for n in range(1, a.runs + 1):
        for i, case in enumerate(cases(a.cases)):
            arms = ARMS if i % 2 == 0 else ARMS[::-1]  # alternate order so nothing rides on it
            jobs += [(case, arm, n) for arm in arms]
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        for line in pool.map(lambda j: review(out, *j), jobs):
            print(line, flush=True)


JUDGE = """You grade one code review against an answer key written before the review existed. Grade only what the review says; do not reward length, tone or format.

ANSWER KEY
{key}
THE CODE THAT WAS REVIEWED
{src}

THE REVIEW
{review}

Instructions:
- A "must" item is "hit" when the review reports that defect as a finding (any section except an explicitly unverified or speculative one) with its location and a correct mechanism; "partial" when it is reported but the mechanism or impact is wrong, or it appears only as unverified or speculative; otherwise "miss".
- List every decoy (D*) and good-code item (G*) the review reports as a defect or as something to change, at any severity, including optional or minor suggestions.
- List every taste item (T*) the review reports as a finding or suggestion.
- List every extra (X*) the review reports.
- List every other finding or suggestion not matched to the key. For each, judge it against the code: "real" (a genuine defect, or a change with a concrete cost), "false" (wrong, or preference with no cost), or "unsure".
- "clean_verdict": true when the review's overall conclusion is that no changes are needed (optional nits listed alongside count as not clean).
- "severity_ok": false when a must item it found is ranked below a finding that is only an improvement or a style point, or a taste item is ranked as a bug.
Answer with JSON only, no prose, in this shape:
{{"must": {{"M1": "hit|partial|miss"}}, "decoys_flagged": ["D1"], "good_flagged": ["G1"], "taste_flagged": ["T1"], "extras": ["X1"], "unmatched": [{{"finding": "...", "verdict": "real|false|unsure", "why": "..."}}], "clean_verdict": false, "severity_ok": true, "notes": "one sentence"}}"""


def source(fixture):
    root, parts = fixture_dir(fixture), []
    for d, dirs, files in sorted(os.walk(root)):
        dirs[:] = sorted(x for x in dirs if x != "__pycache__")
        for f in sorted(files):
            p = os.path.join(d, f)
            parts.append(f"\n===== {os.path.relpath(p, root)}\n" + open(p).read())
    return "".join(parts)


def grade(out, bid, run):
    fixture, key, _ = read_case(run["case"])
    prompt = JUDGE.format(key=key, src=source(fixture), review=run["review"])
    proc = subprocess.run(["claude", "-p", prompt, "--model", JUDGE_MODEL, "--restricted", "--strict-mcp-config",
                           "--tools", "", "--output-format", "json"],
                          stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=JUDGE_TIMEOUT)
    text = json.loads(proc.stdout)["result"]
    grade = json.loads(re.search(r"\{.*\}", text, re.S).group(0))
    json.dump(grade, open(os.path.join(out, "grades", bid + ".json"), "w"), indent=1)
    return bid


def cmd_judge(a):
    out = os.path.abspath(a.out)
    os.makedirs(os.path.join(out, "grades"), exist_ok=True)
    runs = [json.load(open(os.path.join(out, "runs", f))) for f in sorted(os.listdir(os.path.join(out, "runs"))) if f.endswith(".json")]
    failed = [f"{r['case']} {r['arm']} {r['n']}" for r in runs if not r["ok"]]
    if failed:
        sys.exit("rerun these before judging: " + ", ".join(failed))
    ids = random.sample(range(1000, 10000), len(runs))
    mapping = {f"r{i}": {k: r[k] for k in ("case", "arm", "n")} for i, r in zip(ids, runs)}
    json.dump(mapping, open(os.path.join(out, "mapping.json"), "w"), indent=1)
    order = list(zip(mapping, runs))
    random.shuffle(order)
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        for bid in pool.map(lambda x: grade(out, *x), order):
            print("graded", bid, flush=True)
    unsure = [f"{bid}:{i}  [{m['case']}] {u['finding']}  ||  {u['why']}"
              for bid, m in mapping.items()
              for i, u in enumerate(json.load(open(os.path.join(out, "grades", bid + ".json"))).get("unmatched", []))
              if u["verdict"] == "unsure"]
    print(f"\n{len(unsure)} unsure findings to rule in overrides.json (labels hidden):")
    print("\n".join(unsure))


def cmd_score(a):
    out = os.path.abspath(a.out)
    mapping = json.load(open(os.path.join(out, "mapping.json")))
    path = os.path.join(out, "overrides.json")
    overrides = json.load(open(path)) if os.path.exists(path) else {}
    rows, open_items = {}, []
    for bid, m in mapping.items():
        g = json.load(open(os.path.join(out, "grades", bid + ".json")))
        run = json.load(open(os.path.join(out, "runs", f"{m['case']}-{m['arm']}-{m['n']}.json")))
        verdicts = []
        for i, u in enumerate(g.get("unmatched", [])):
            v = overrides.get(f"{bid}:{i}", u["verdict"])
            if v == "unsure":
                open_items.append(f"{bid}:{i}")
            verdicts.append(v)
        must = g.get("must", {})
        hits = sum(v == "hit" for v in must.values())
        part = sum(v == "partial" for v in must.values())
        noise = len(g.get("decoys_flagged", [])) + len(g.get("good_flagged", [])) + len(g.get("taste_flagged", [])) + verdicts.count("false")
        true = hits + part + len(g.get("extras", [])) + verdicts.count("real")
        rows[(m["case"], m["arm"], m["n"])] = {
            "recall": (hits + 0.5 * part) / len(must) if must else None, "found": {k for k, v in must.items() if v == "hit"},
            "noise": noise, "items": true + noise, "precision": true / (true + noise) if true + noise else 1.0,
            "clean": bool(g.get("clean_verdict")), "tokens": run.get("tokens", 0)}
    if open_items:
        sys.exit("rule these in overrides.json first: " + ", ".join(open_items))

    def jaccard(sets):
        pairs = list(itertools.combinations(sets, 2))
        return st.mean(len(x & y) / len(x | y) if x | y else 1.0 for x, y in pairs) if pairs else None

    by_case, names = {}, sorted({c for c, _, _ in rows})
    print(f"{'case':20}{'arm':6}{'recall':>8}{'noise':>7}{'prec':>7}{'clean':>7}{'consist':>9}{'tokens':>9}")
    for c in names:
        for arm in ARMS:
            r = [v for (cc, aa, _), v in rows.items() if cc == c and aa == arm]
            rec = [x["recall"] for x in r if x["recall"] is not None]
            row = {"recall": round(st.mean(rec), 3) if rec else None, "noise_per_run": round(st.mean(x["noise"] for x in r), 2),
                   "precision": round(st.mean(x["precision"] for x in r), 3), "clean": f"{sum(x['clean'] for x in r)}/{len(r)}",
                   "consistency": round(jaccard([x["found"] for x in r]), 2) if rec and len(r) > 1 else None,
                   "tokens_median": int(st.median(x["tokens"] for x in r))}
            by_case.setdefault(c, {})[arm] = row
            print(f"{c:20}{arm:6}{str(row['recall']):>8}{row['noise_per_run']:>7}{row['precision']:>7}{row['clean']:>7}{str(row['consistency']):>9}{row['tokens_median']:>9}")
    arms = {}
    for arm in ARMS:
        r = [v for (_, aa, _), v in rows.items() if aa == arm]
        rec = [x["recall"] for x in r if x["recall"] is not None]
        arms[arm] = {"recall": round(st.mean(rec), 3), "noise_per_run": round(st.mean(x["noise"] for x in r), 2),
                     "items_per_run": round(st.mean(x["items"] for x in r), 2),
                     "not_worth_fixing_share": round(sum(x["noise"] for x in r) / max(1, sum(x["items"] for x in r)), 3),
                     "precision": round(st.mean(x["precision"] for x in r), 3), "tokens_median": int(st.median(x["tokens"] for x in r))}
        print(arm, arms[arm])
    json.dump({"arms": arms, "by_case": by_case, "meta": json.load(open(os.path.join(out, "meta.json")))},
              open(os.path.join(out, "scores.json"), "w"), indent=1)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--old", help="git ref for the old agent; default the newest tag")
    r.add_argument("--runs", type=int, default=3)
    r.add_argument("--jobs", type=int, default=9)
    r.add_argument("--cases", type=lambda s: s.split(","), help="comma-separated case names; default all")
    j = sub.add_parser("judge")
    j.add_argument("--jobs", type=int, default=9)
    s = sub.add_parser("score")
    for parser in (r, j, s):
        parser.add_argument("subject", help="a subagent name, as in subagents/<name>.md")
        parser.add_argument("out")
    a = p.parse_args()
    global SUBJECT, HERE, AGENT
    SUBJECT, HERE, AGENT = a.subject, os.path.join(BENCH, a.subject), f"subagents/{a.subject}.md"
    if not os.path.isfile(os.path.join(ROOT, AGENT)) or not os.path.isdir(os.path.join(HERE, "cases")):
        sys.exit(f"no subagents/{a.subject}.md or no bench/{a.subject}/cases")
    {"run": cmd_run, "judge": cmd_judge, "score": cmd_score}[a.cmd](a)


if __name__ == "__main__":
    main()
