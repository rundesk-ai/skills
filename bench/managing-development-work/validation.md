# Managing Development Work Validation

The cases under `cases/` are the benchmark; results are under
`bench/results/managing-development-work/`, and `./scripts/bench-status.sh managing-development-work`
says whether the newest one still measures the current skill.

## Boundary under test

The skill should activate for taking on, sizing, slicing, delivering, resuming or finishing a
software change. It should not activate for diagnosing a failure of unknown cause, writing a ticket
for people to read, or answering a question about the code.

## What each case covers

| Case | Covers |
|---|---|
| q01-easy | Direct work stays light: no slice list, plan or brief for a known-cause fix |
| q02-medium | Large work is sized and sliced before code; riskiest slice first; one slice proven before the next |
| q03-complex | A grab-bag request split into separate outcomes, with no code written |
| q04-ladder | The least-work order: reuse and the standard library before new code |
| q05-ticket | A ticket's Done when lines kept as the proof and each traced to evidence |
| q06-resume | Resuming from an existing brief: first unproven slice, decisions kept, stale next action caught |
| q07-handoff | Work left for a later session: a brief written where the next session looks |
| r01–r04 | Routing: direct, indirect, near miss, and a resume request |

## Not yet covered

Delegating and integrating returned work, a boundary that must grow mid-slice, and the named-risk
responses in `references/coordination.md` have no case.
