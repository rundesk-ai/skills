# Benchmark a skill against live agents

## Skill

> Replace this line with the name of one skill in `skills/`.

Measure whether the skill above fires when it should, and whether the agent that loads it does
better work than it would unaided — on every agent installed on this machine — and record the result
under `bench/results/`. One skill per run: a result that mixes two says nothing about either. If
the line above still reads as the instruction to replace it, ask which skill and stop.

## Before starting

1. Load `writing-skills` and read `references/evaluating.md` in full. It owns the method; this prompt
   adds the harness, the agents and the record.
2. Hold to the design every benchmark here follows. It takes two measurements: whether the skill
   fires, since its description is the whole trigger and a skill that never loads cannot help; and
   whether it improves the work, by running each case twice, with the skill available and without, and
   having a judge grade both against the case's rubric. The control arm is what separates a skill that
   helps from a task the model already does well. A case is a task prompt under
   `bench/<skill>/cases/`, with front matter naming the skill, the variant if any, and the rubric. No
   runner exists yet, so you are the runner until one does; before writing one, assess whether
   `claude plugin eval` fits, since it already hosts eval suites with a JSON report and a sandbox.
3. Read the skill in full, so the cases test what it claims rather than what you assume.

## What is measured

A skill is guidance an agent pays for in tokens. The question a benchmark answers is not "is it
good" but **how much quality it buys for what it costs**, so a run reports three numbers and the
ratio between them. All three are measured per agent: a description that routes on one agent can be
invisible on another.

### Cost, in tokens

| Paid | When | How it is read |
|---|---|---|
| **Standing** | every session, whether or not the skill fires | the same trivial prompt in a directory with the skill and one without; the difference in input tokens is the description |
| **Load** | when it fires | the body, from the file |
| **Depth** | when a reference is opened | the references the transcript shows being read |
| **Run** | the whole task | what the agent reported using, with the skill and without |

Standing cost is the one that never sleeps. A description that costs 130 tokens is paid on every
turn of every session in every project the skill is pushed into, and is the first thing to cut.

### Routing, 0 to 1

A fixed set of requests, each with the decision it should produce. Correct decisions divided by
cases. **A skill that fires when it should not is as wrong as one that never fires**, and both cost:
one spends the whole task, the other spends the body and the attention it took to read it.

| Case | Shape |
|---|---|
| Direct | the work, named the way the description names it |
| Indirect | the same work, in words that never use the skill's vocabulary |
| Adjacent | work a neighboring skill owns, which this one must leave alone |
| Out of scope | work the description explicitly declines |
| Edge | a request carrying the skill's words while meaning something else |

Record whether the skill was discovered separately from whether it fired. A skill the agent never
saw is a deployment fault; a skill it saw and passed over is a description fault, and they are fixed
in different places.

### Quality, 0 to 1

Cases at three difficulties, because a skill usually earns nothing on the easy one:

| Difficulty | The case |
|---|---|
| **Easy** | one fact, one source, an answer that is right or wrong |
| **Medium** | several sources that must be reconciled, with a disagreement in them |
| **Complex** | a question the evidence cannot fully settle, where the work is scoping it, separating what is known from what is inferred, and saying what is unresolved |

Each case is graded against a rubric written before the first run, and the rubric scores two things
separately: **the result**, which is what the reader gets, and **conduct**, which is whether the
agent did what the skill says — the steps it names, in the order it names them. A good answer
reached by ignoring the skill is a skill that changed nothing.

Run each case with the skill and without it. Quality is the skilled arm's score; the number that
matters is the **delta** against the control.

### Value

```text
value = quality delta / (run tokens with the skill - run tokens without) x 1,000,000
```

Quality points bought per million extra tokens, which is the scale a real difference lands on: a
skill that opens four references and runs a dozen searches spends hundreds of thousands of tokens
to move a rubric by a fraction of a point. Report value per difficulty — the same skill is often
worthless on an easy case and decisive on a hard one, and one averaged number hides that.

`score` is the mean quality delta across the difficulties: what the skill is worth on the work,
before its cost is weighed against it.

### Consistency

Run each quality case three times per arm and report the spread. A skill exists so that the same
request gets the same standard of work twice, so a wide spread in the skilled arm is a finding even
when the mean improved.

### Comparing runs over time

A score means nothing alone; it means something against the last one. Keep the cases and rubrics
frozen and record `cases_version` with every result. When a case or rubric changes, raise the
version and say in the report that earlier numbers no longer compare.

## The agents

Detect what is installed; never assume. Record each version in the result, because a benchmark
against an unnamed version cannot be repeated.

```sh
for c in claude codex grok; do command -v "$c" >/dev/null && "$c" --version; done
```

| Agent | Single-turn run | Reads skills from |
|---|---|---|
| `claude` | `claude -p "<prompt>" --output-format json` | `.claude/skills/` |
| `codex` | `codex exec "<prompt>" --skip-git-repo-check` | `.agents/skills/` |
| `grok` | `grok -p "<prompt>" --output-format json` | `.agents/skills/` |

Add `--model` to pin the model, and hold one model per agent across both arms of every case. An
agent that is not installed is skipped with a line in the result saying so — never with a zero,
which reads as a measurement.

## Write the cases

Cases live in `bench/<skill>/cases/`, one file each, with front matter naming the skill, the variant
if any, and the rubric to grade against:

```markdown
+++
skill = "testing-code"
variant = ""
rubric = """
1. Names the boundary the test sits at, and why that one.
2. Asserts on behavior a person would notice, not on an internal call.
3. Proves the test fails for the reported reason before the fix.
"""
+++
The `orders` endpoint sometimes returns a total that is a cent short. Add a test.
```

- **Three cases at least**, carrying the mess a real request carries. A task built to show the skill
  working proves only that.
- **One near-miss case** whose front matter says the skill must *not* fire, drawn from the boundary
  its description declines. A skill that fires on everything is as broken as one that never fires.
- **Write the rubric before the first run.** A rubric written after reading the output grades the
  output it was written from.

## Run it

For each agent, for each case, run both arms:

1. Make a fresh empty directory for every run. A run that reuses a directory inherits the last one's
   files, and the agent reads them.
2. **With the skill:** `./scripts/deploy.sh <dir> <skill>` — it writes `<dir>/.agents/skills/` and
   a `.claude/skills` link to it for Claude, so every agent reads one copy. It refuses a directory
   inside a git checkout, so make the run directories outside one.
3. **Without the skill:** the same directory contents, no `.agents/skills/`.
4. Same prompt, same model, same inputs, no hints. Alternate which arm runs first across cases, so
   nothing systematic rides on order.
5. **Three runs per arm.** One run of each is an anecdote; the spread between runs is what says
   whether a difference is real.
6. Capture what each run produced — the files, not the agent's account of them — and the transcript.

**Whether it fired** is read from the transcript: for `claude`, the JSON output names the skill when
it loads; for `codex` and `grok`, look for the skill's own words and steps in the run. Where an agent
gives no way to tell, record `unknown` rather than a guess.

## Grade it

Grade with a judge that is given the rubric and both outputs **with the arms unlabeled**, so it
cannot reward the one it expects to win. For each case and agent, record better, same or worse, and
one sentence saying what differed. Read the artifacts yourself before accepting the verdict: an
agent's summary of its own work is generous about what it skipped.

Three outcomes, and each means something different:

- **The skilled run is better.** Name the part of the skill that did it. That part is proven; the
  rest is not.
- **The runs are indistinguishable.** Either the task did not need the skill, or the skill restates
  what the agent already does. That is the most common kind of dead weight, because it reads as
  sensible in review.
- **The skilled run is worse.** Usually over-specification: a rule stated without its reason, applied
  literally to a case it was never meant for.

## Record it

Write one file per run to `bench/results/<skill>/<YYYY-MM-DD>.json`. `date` and `score` are the
two keys every later reader of the results relies on, so they are the contract:

```json
{
  "date": "2026-09-19",
  "skill": "testing-code",
  "score": 0.72,
  "cases": 4,
  "agents": {
    "claude": {"version": "2.1.278", "model": "…", "fired": "3/3", "near_miss_fired": false,
               "better": 2, "same": 1, "worse": 0, "score": 0.67},
    "codex":  {"version": "0.154.0", "model": "…", "fired": "2/3", "near_miss_fired": false,
               "better": 1, "same": 2, "worse": 0, "score": 0.33},
    "grok":   {"skipped": "not installed"}
  },
  "notes": "one line per case saying what differed"
}
```

`score` is the share of cases where the skilled arm was judged better, averaged over the agents that
ran, to two decimals. A near miss that fired counts against the score, because a skill that steals
another's trigger costs every task it interrupts.

## Report

1. One line: the skill, the agents and versions that ran, the cases, and the score.
2. A row per agent: fired, near miss, better/same/worse, score.
3. The part of the skill each improvement came from.
4. Every case where the runs were indistinguishable, and what you propose cutting.
5. What could not be measured, and why.

Do not edit the skill in the same run as the benchmark. Measure, report, and change it afterwards —
a skill tuned against the cases it was measured on handles those cases and nothing else.
