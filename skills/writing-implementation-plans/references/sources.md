# Sources

These sources establish the planning traps and replacements synthesized in
`SKILL.md`; they are not a substitute for repository inspection.

## Plan quality and change

- [NASA Software Engineering Handbook, SWE-013: Software Plans](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695397/SWE-013+-+Software+Plans)
  says software plans should be complete, correct, workable, consistent, and verifiable; should
  identify work, commitments, and risks; and must be maintained as requirements, resources, or
  solutions change. This supports the execution contract, requirement trace, and explicit
  assumptions rather than vague or frozen plans.
- [Principles behind the Agile Manifesto](https://agilemanifesto.org/principles) makes working
  software the primary measure of progress and expects changing requirements. This supports
  outcome-based proof and plans short enough to revise, not speculative implementation transcripts.
- Ken Schwaber and Jeff Sutherland's [Scrum Guide](https://scrumguides.org/scrum-guide.html) treats
  the Sprint Backlog as a real-time plan that is updated as work and knowledge change, with progress
  measured against a definition of done. This supports concise task states, proof before
  `completed`, and revising downstream work instead of appending a progress diary.

## Decomposition and proof

- [Google Engineering Practices: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
  reports that small, self-contained changes are easier to review, reason about, merge, and roll
  back. Its concrete guidance keeps related tests with behavior, orders dependent changes, and adds
  coverage before refactoring untested code. This is the basis for the good/bad decomposition pair.
- George Pirocanac's [How Much Testing Is Enough?](https://testing.googleblog.com/2021/06/how-much-testing-is-enough.html)
  distinguishes unit, integration, and end-to-end evidence, and warns that code coverage alone does
  not establish absence of bugs. This supports naming the behavior and expected observation instead
  of writing only `run tests` or relying on a percentage.
- Wei Zhang and Jessie Jie Xia's [Abstraction first](https://martinfowler.com/articles/structured-prompt-driven/abstraction-first.html)
  identifies unclear boundaries, responsibilities, interfaces, and dependencies as sources of AI
  rework. It recommends atomic, testable, acceptance-ready tasks grounded in the existing technical
  context. This practitioner guidance supports inspection before decomposition and complete,
  independently checkable tasks.

## Authority boundary

- [NIST SP 800-171 Rev. 3, 03.01.05–03.01.07](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/800-171r3/NIST.SP.800-171r3.html)
  limits access and privileged functions to authorized duties. Applied here: a plan names required
  approval and responsibility for privileged operations; it never treats the plan itself as
  authorization.

## Agent workflow comparison

- OpenAI's [model guidance](https://developers.openai.com/api/docs/guides/latest-model) recommends
  outcome-focused instructions that state the goal, context, constraints, evidence, success
  criteria, and approval boundaries. It does not prescribe a Codex implementation-plan document
  format; this skill therefore keeps those transferable inputs without claiming an official schema.
- Anthropic's [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) frames
  agent work as gathering context, acting, and verifying, and recommends exploring before complex
  implementation. Its [common workflows](https://code.claude.com/docs/en/common-workflows) and
  [CLI reference](https://code.claude.com/docs/en/cli-usage) separate read-only planning from edits
  until approval. This supports investigation before sequencing and treating a plan as a reviewable
  artifact distinct from execution, without importing product-specific commands or conventions.

## The least-work rule

- Dietrich Gebert's [Ponytail](https://github.com/DietrichGebert/ponytail) (MIT) takes, after reading
  the code a change touches, the first option that fully works — no new code, existing code, the
  standard library or platform, an installed dependency, one line, then the minimum new code — and
  never cuts validation, data-loss handling, security or accessibility. Its author-run benchmark
  reports roughly half the code with more risky logic tested. This skill applies the same order when
  choosing each task, so the plan, not the implementer, removes the unneeded work.
- Martin Fowler's [Yagni](https://martinfowler.com/bliki/Yagni.html) explains the cost of building a
  capability before it is needed, supporting the **Not built** line and the rule against "for later" tasks.
