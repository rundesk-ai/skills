# Tracking

A brief is the smallest current record that lets you, or the next session, resume the outcome
without rebuilding its scope from the conversation. It is execution state, not a second task
tracker and not a log.

## When to keep one

Keep one when a slice will still be open at the end of the turn — deferred and `~` slices included —
when part of the work is delegated, or when the owner asks for it. Do not when the work finishes in
this turn, or when an existing tracker already holds the scope, state, next action and proof.
When a ticket or plan exists, link it and keep only the execution state it does not hold; a stale
brief never overrides its source.

## Where it lives

A brief exists for the next session, so it must be somewhere that session will look. A scratch
directory tied to the current session is gone by then. Take the first of these that exists:

1. The location the owner or the repository rules name.
2. A task, memory or notes store the environment keeps across sessions for this project.
3. Otherwise, ask the owner once where briefs go, offering a git-ignored directory in the project.
   Until they answer, write it in the working area and say in your reply that it will not survive the
   session.

Never commit a brief unless the repository rules say to: it is execution state, not project history.
Name it `YYYY-MM-DD-<outcome>.md`; one brief per outcome, updated in place.

## Shape

```markdown
# <Outcome>

**Status:** active | waiting | blocked
**Source:** <ticket link or the request>
**Last checked:** YYYY-MM-DD HH:MM

## Done when
## Slices
## Decisions
## Next action
## Blocked on
```

Write current facts. **Slices** is the slice list with each one's rung, state and observed proof.
**Decisions** holds only choices a later session must not reopen.

## When to update it

After a slice is proven, a decision changes, a delegation goes out or comes back, a blocker appears,
or before ending a turn with work unfinished — then make **Next action** executable. Do not record
routine tool calls or chronology: they make stale instructions look current.

## Resuming

Look for a brief at the start of any work, in the places above, matched by outcome rather than by
the words of the new request: "carry on with the invoices", "where were we" and a bare ticket number
all point at an existing one. Check the repository's working state and branches as well; commits
with no brief are work in progress too.

1. Read the source and the brief; confirm they still describe the same outcome.
2. Reconcile anything newer: a changed requirement, external state, a returned delegation.
3. Check the next action against the actual files and systems before acting.
4. Continue from the first unproven slice.

## Closing

Remove the brief once the outcome's proof passes or the owner cancels it. Move durable decisions and
final evidence to the ticket or project first. A finished brief left behind becomes misleading state.
