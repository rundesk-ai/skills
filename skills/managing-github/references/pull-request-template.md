# Fallback GitHub pull-request template

Use this only when the target repository has no applicable pull-request template. A reviewer decides
in under a minute whether to read the diff, so the body says what changed and why, and how it was
checked — never what the diff already shows.

````md
## Summary

<!-- What was wrong or missing, and what is true now. One or two sentences. -->

## Changes

- <!-- One change per bullet, as someone using it would notice it — not a file list. -->

## Testing

- [x] <!-- Each check run on this exact head, with what it showed. -->
- [x] Required GitHub checks pass for the exact head commit.

<!-- One standalone `Closes #<number>.` line per completed issue; `Refs` for partial work. -->
````

- Put **Breaking:** or **Risk:** as one bold line under **Changes** when the change breaks a public
  contract or carries a security, privacy, data, billing, destructive or deployment risk. A risk in
  the middle of a paragraph goes unread.
- Leave a check unticked and say why when it could not be run. A ticked box is a claim that it ran.
- Append nothing after the last section — no agent name, identity block, generated-by footer or
  co-author line. The change is judged on the diff, not on who typed it.
