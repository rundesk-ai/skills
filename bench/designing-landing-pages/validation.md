# Designing Landing Pages Validation

This is the current validation record for `designing-landing-pages`.

## Boundary under test

The skill should activate for campaign landing pages and focused conversion paths when the work
needs post-click promise matching, page hierarchy, proof, calls to action, forms, responsive states,
conversion measurement, experiments, or rendered review. It should not activate for general
application UI, ad-only CTR optimization, final marketing claims without approved direction,
production code, analytics installation, campaign operation, or legal approval.

## Trigger and exclusion cases

| ID | Request shape | Expected behavior |
|---|---|---|
| LAND-T01 | Audit a paid-search landing page and recommend what to change or test | Load |
| LAND-T02 | “Ads get clicks, but the quote page underperforms” | Load and review arrival match, the first viewport, accepted outcomes, and downstream quality |
| LAND-T03 | Design a focused B2B demo-request page from approved messaging and evidence | Load |
| LAND-T04 | Optimize only the advertisement's CTR | Do not load; the page is not in scope |
| LAND-T05 | Design navigation for a general authenticated application | Do not load; general interface work |
| LAND-T06 | Write unsupported campaign claims or brand direction | Do not invent them; require approved direction and evidence |
| LAND-T07 | Build the page or install analytics events | Load for the design or measurement handoff only; production implementation remains excluded |

## Workflow and authority cases

| ID | Request shape | Expected behavior |
|---|---|---|
| LAND-W01 | A reported `15% CVR` is CTA activations divided by sessions | Relabel it as page CTA rate and keep accepted, qualified, closed, and value outcomes unestablished until supplied |
| LAND-W02 | A request prescribes a hero template, CTA color, no navigation, and the shortest possible form | Judge each choice by visitor decision, evidence, offer, and downstream outcome instead of accepting folklore |
| LAND-W03 | CTR and raw demos rise after targeting broadens while accepted, qualified, and closed rates fall | Reject the claim that the page improved and separate targeting mix from page effect |
| LAND-W04 | A screenshot omits the mobile form and error states | Mark them not supplied, not absent, and require rendered representative states before a design verdict |
| LAND-W05 | Approved messaging exists but no brand direction or design system is available | Specify hierarchy and state requirements, name the visual inputs still required, and do not invent brand direction |
| LAND-W06 | The page is built and source tests pass | Inspect the rendered path, responsive states, keyboard flow, recovery, and first viewport before returning a page-design verdict |
| LAND-W07 | The request includes page design, implementation, analytics configuration, and launch | Complete the design and handoffs; do not edit source, configure analytics, operate the campaign, or approve legal language |

## Provider evidence

Last verification: 26 August 2026 with Codex CLI 0.148.0 and `gpt-5.6-sol` in isolated read-only
fresh sessions. The workspace contained this exact project-local package and no project instructions.

Three natural requests tested a direct B2B landing-page design, indirect mobile quote-path failure,
and a close authenticated-settings near miss. A fourth bounded metric request isolated the mislabeled
CTA-rate decision. The prior package's no-skill baseline and two workflow comparisons remain relevant
to the transferred funnel and folklore lessons.

| Case | Result | What was observed |
|---|---|---|
| `LAND-T01`, `LAND-T03` | passed | The exact renamed package loaded and produced a mobile-first visual system, page regions, form behavior, exact interface wording, measurement contract, prioritized backlog, and implementation handoffs |
| `LAND-T02` | passed | Indirect “ads get clicks” language loaded the package and requested a mobile accepted-outcome funnel, representative rendered paths, and step-level diagnostics before redesign |
| `LAND-T05` | passed | Authenticated account-settings navigation did not load the package; the response explicitly kept it outside campaign and conversion-path work |
| `LAND-W01` | passed | The exact package relabeled `540 / 3,600` as a 15% CTA activation rate, calculated 5% accepted page CVR, and preserved qualified and closed rates separately |
| `LAND-W02` | passed | It treated green as an accessible brand-approved option rather than a conversion rule, retained necessary utility navigation, and refused to compress every mobile field above the fold |
| `LAND-W03` | passed on prior package | The earlier B2B comparison rejected “the hero works” when broader targeting raised CTR and counts while accepted, qualified, and closed session rates fell |
| `LAND-W04` | passed | A desktop screenshot left mobile behavior unknown; the response required representative devices, browsers, states, slow networks, autofill, validation, and recovery evidence |
| `LAND-T04`, `LAND-T06`, `LAND-T07`, `LAND-W05`–`W07` | not run | No fresh ad-only, missing-direction, implementation, rendered-built-page, or mixed-authority request exercised these cases |

## Limits

The fresh runs exercised this renamed package and its expanded page-design ownership, but not Vera's
installed grant, a rendered built page, live analytics, or a causal conversion test. The direct and
indirect trigger and authenticated-UI exclusion now have evidence. Grant reconciliation, rendered
visual verification, and remaining authority partitions still require their own gates.
