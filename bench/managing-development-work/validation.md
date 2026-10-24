# Managing Development Work Validation

The cases under `cases/` are the benchmark; results are under
`bench/results/managing-development-work/`, and `./scripts/bench-status.sh managing-development-work`
says whether the newest one still measures the current skill.

## Boundary under test

The skill should activate for taking on, sizing, slicing, delivering, resuming or finishing a
software change, including handing parts of it to other agents. It should not activate for
diagnosing a failure of unknown cause, writing a ticket for people to read, or answering a question
about the code.

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
| q08-delegate | Parallel delegation: separate edit boundaries, self-contained handoffs, returned work checked before it is reported |
| r01–r05 | Routing: direct, indirect, near miss, a resume request, and a request to hand work to subagents |

## Not yet covered

A boundary that must grow mid-slice, and the named-risk responses in `references/coordination.md`,
have no case.
