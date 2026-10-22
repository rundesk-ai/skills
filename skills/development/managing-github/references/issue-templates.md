# Fallback GitHub issue templates

Use one of these only when the target repository has no template for the issue's kind. They match
the shapes used for bug and task tickets in other trackers, so an issue reads the same wherever it is
filed. Select one form, replace every comment, remove placeholders, and preserve the headings in
order. Drop **Not included** when nothing needs saying.

## Bug report

```md
## Problem

<!-- What goes wrong and for whom, then what it costs. Two sentences. -->

## Steps to reproduce

<!-- From a known starting state, one action per step. If it has not been reproduced, say so instead of guessing steps. -->

## Expected

<!-- What should happen. -->

## Actual

<!-- What happens instead, quoting the exact error. -->

## Tested

<!-- Where it fails, where it does not, how often, and when it started if known. Mark unknowns rather than guessing. -->

## Done when

<!-- Pass-or-fail outcomes, starting with the steps above giving the expected result. -->

## Not included

<!-- Only what a reader might assume is part of this fix. -->
```

## Feature request

```md
## Problem

<!-- What is missing or wrong today and what it costs. Two sentences. -->

## Goal

<!-- What is true once this is handled. One sentence. -->

## Done when

<!-- One pass-or-fail outcome per line that someone can check, with no implementation steps. -->

## Not included

<!-- Only what a reader might assume is part of this but is not. -->
```

The issue title names the outcome or the symptom — "Keep quote answers on Back in mobile Safari" —
not the fix. Put a suspected cause or a possible approach in a clearly labelled comment, never in
the body's requirements. Never include credentials, personal data, private identifiers or
owner-specific paths.
