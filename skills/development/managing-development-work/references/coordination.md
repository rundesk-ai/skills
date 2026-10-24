# Coordination

## Risk responses

Name the trigger and add only its evidence. Do not route every change through a fixed sequence of
specialists.

| Trigger | Required response |
|---|---|
| Authentication, authorization, secrets, privacy | Trace trust boundaries, redaction and refusal paths. |
| Money, entitlement, irreversible business state | Preserve invariants and define reconciliation. |
| Schema, migration, deletion, stored data | Define compatibility, recovery and post-change checks. |
| Production, infrastructure, deployment | Separate implementation from rollout; define rollback and health proof. |
| Public API, format, integration | Identify the actual consumers and prove compatibility. |
| Concurrency, performance, broad blast radius | Measure a representative baseline and the relevant limit. |

## When the boundary must grow

If the outcome genuinely needs a larger boundary, stop before changing it. Present the smallest
viable expansion, why the original boundary fails, the contracts affected, the risks, alternatives
and proof. Sunk effort and passing tests do not authorize new scope. For an explicit refactor,
characterize preserved behavior first and change it in reversible steps.

## Delegating

Keep decisions, dependency order, integration and the final report with one responsible agent. Use
one implementer per phase; parallelize only phases with separate edit boundaries, when the value beats
the coordination cost. Work across repositories or across more than one material risk becomes
separate, ordered phases, each leaving a coherent result with its own proof.

Write each handoff so an engineer who never saw this conversation could finish the part from it
alone, because that is the delegate's position. Fill every line; a line left out is a decision the
delegate makes by guessing.

```markdown
Goal: <one testable outcome, and why the requester wants it>
Context: <what you already know or ruled out, and the files to read first>
Boundary: <the files it may change; what it must not touch, and who else is editing what>
Constraints: <repository rules and skills that apply, compatibility, dependencies, actions it is not authorized to take>
Decided: <choices already made, so it does not reopen them; choices left to it, to state in its report>
Done when: <the exact checks and commands, run by the delegate, that prove the part>
Stop: <when to stop, and what to bring back instead of deciding: a boundary that must grow, a scope question>
Report: <the diff or changed files, each Done when line with its output, what was skipped or not checked>
```

For investigation or review, hand over the question and the evidence, not the answer you expect: a
delegate given your hypothesis tends to return it confirmed. Send review to a reviewer only once the
integrated change is inspectable, naming the exact base and head, the acceptance criteria and the
few invariants most at risk.

## Integrating

A returned summary is not integration. Inspect the full diff, the surrounding contracts and the
reported evidence; rerun the narrowest meaningful checks and then the repository's gate on the
integrated result; exercise a safe representative path. Allow a focused correction for a contained
miss; if the correction reveals a different design, re-scope instead of layering patches.
