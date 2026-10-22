---
name: game-management-sims
description: Use when designing or critiquing a city-builder, colony sim, factory game, tycoon game, settlement game, or another systemic management game, including what deserves simulation, binding-constraint and nested management loops, indirect control, crises and recovery, agent-versus-aggregate representation, explainability, or automation that removes busywork without removing decisions. It supplies an experience-led workflow and testable hypotheses. Do not use it for simulation implementation, runtime scheduling, UI implementation, general game design alone, or playtest execution.
---

# Design systemic management games

Make the simulated world a decision generator. Depth comes from understandable relationships that
create new tradeoffs, not from the number of resources, citizens, recipes, or background variables.
Treat every claim about enjoyment as an audience-specific hypothesis to test.

## Set the management promise

Start from the game's experience contract, then specify:

- **Managed subject:** what the player identifies with—a person, household, organization, settlement,
  network, ecosystem, or world—and what remains outside their authority.
- **Role and verbs:** what the fiction permits the player to inspect, place, prioritize, budget,
  schedule, forbid, automate, or delegate.
- **Experience hypotheses:** the intended forms of autonomy, competence, curiosity, attachment,
  tension, recovery, and expression, with observable supporting and contradicting behavior.
- **Time horizons:** what decisions recur within seconds, minutes, a session, and the long game.
- **Non-goals:** realism, population scale, simulation detail, or content breadth that the promise does
  not need.

Choose the subject before copying genre conventions. A city treated as the player's avatar needs
different stakes and progression from a game whose promise depends on particular citizens and their
histories.

## Budget simulation detail by player value

For every proposed system, write this chain:

```text
player-visible state -> decision it changes -> system consequence -> readable evidence -> next decision
```

Keep the minimum representation that can produce the promised decisions or stories. Add fidelity
when players can perceive the distinction, act differently because of it, and trace a consequence
back to it. Collapse or remove detail that only consumes computation, authoring, interface attention,
or debugging effort.

Choose agent, aggregate, or hybrid representation as a player-design decision:

- Use named or persistent agents when individual location, history, relationships, or loss supports
  attachment, diagnosis, or meaningful intervention.
- Use aggregates when only a population-level stock, rate, capacity, or trend changes the decision.
- Use a hybrid when representative agents carry visible stories while aggregate rules own scale.

Do not promise a simulated individual when the player sees only a counter. Do not add thousands of
agents merely to claim realism. Authoritative state, scheduling, spatial indexing, and simulation
levels of detail are simulation engineering, not design decisions.

```text
Good: retain individual workers because following one route exposes transport and staffing failures.
Bad:  simulate every worker's invisible preferences, then show only total productivity.
```

## Design coupled constraints, not isolated meters

Map the system as stocks, flows, capacities, networks, policies, delays, risks, and feedback
relationships. For each relationship, define what players can observe, which lever they control, how
long resolution takes, what it costs elsewhere, and what new state it creates.

Build the recurring management loop around a changing binding constraint:

```text
observe symptoms -> diagnose the limiting relationship -> form a hypothesis
-> commit a constrained intervention -> let the world resolve over time
-> compare outcome with expectation -> adapt or restructure
```

An intervention should usually move pressure rather than erase it: faster production may consume
more transport, labor, energy, space, maintenance, or political tolerance. Avoid one upgrade that
dominates every state and meters that rise independently without changing another decision.

## Connect nested management loops

Design at least three connected horizons where the game supports them:

1. **Operational:** inspect an exception, reprioritize work, reroute supply, or contain an incident.
2. **Management:** allocate capacity, redesign a network, change staffing, or choose a production mix.
3. **Strategic:** specialize, expand, change policy, accept a constituency cost, or restructure the
   system so recurring failures stop.

A recurring operational symptom should expose a management cause; repeated management pressure
should reveal a strategic choice. If the player repeatedly clears the same alarm after understanding
it, the game is charging attention without generating another decision.

## Make indirect control trustworthy

For every command, policy, priority, zone, schedule, budget, or placement tool, define:

```text
player intent -> eligible actors or systems -> selection rule -> latency and uncertainty
-> visible execution -> completion, refusal, interruption, and recovery
```

Preserve autonomy only where its variance creates useful decisions or character. Explain why an
order waits or fails, show reservations and competing priorities when relevant, and provide a safe
way to revise intent. Do not make the player drag every worker through a system whose promise is
organizational management; do not make autonomous actors ignore explicit priorities without a
legible competing rule.

## Turn crises into tests and transformations

Use crises to stress relationships the player could have understood, not to replace planning with
arbitrary punishment. Define:

- precursor signals and the decision window;
- the capacity, dependency, or policy being tested;
- containment, sacrifice, adaptation, and escape options;
- consequences that change later decisions; and
- a recovery path, transformed stable state, or clear terminal outcome.

Protect against silent death spirals. When loss compounds, expose the feedback path and preserve a
meaningful intervention until the designed point of no return. Permanent failure can serve the
promise, but it still needs attributable causes. Likewise, a solved state needs a deliberate outcome:
expression, expansion, specialization, scenario completion, a new constraint, or a natural stopping
point—not endless manual upkeep.

```text
Good: a drought exposes storage and distribution choices, warns through falling reserves, and leaves
      several costly recovery strategies.
Bad:  delete a random essential building, hide the cause, and call the restart meaningful difficulty.
```

## Make causes inspectable

For every material outcome, design four views:

1. **World signal:** a visible change in agents, buildings, routes, queues, terrain, or activity.
2. **Current state:** the quantity, category, or status that matters now.
3. **Causal trace:** the dominant contributors, blockers, recent changes, and applicable rules.
4. **Forecast and action:** likely direction under current conditions and valid interventions.

Prefer progressive disclosure: the world should reveal that something matters, while overlays and
inspection reveal why. Keep uncertainty when inference is part of the promise, but do not conceal
information required for a decision and later punish the player for lacking it.

## Automate solved execution, not judgment

Classify repeated work:

- Keep a repeated action when context changes its tradeoff and the player still evaluates alternatives.
- Batch, template, schedule, delegate, or automate execution once the choice has become routine.
- Escalate exceptions when an automation cannot meet its policy; do not require constant supervision.
- Preserve preview, cost, priority, pause, override, and rollback where the underlying action needs them.

Automation should raise the player's operating level. If it removes every remaining decision, the
system needs a new horizon or a deliberate completion state—not artificial friction added back in.

## Validate the experience hypotheses

Whitebox complete causal loops before scaling simulation or art. In representative scenarios, test
whether intended players can:

- notice a material symptom and explain its likely cause without team prompting;
- identify multiple plausible interventions and their tradeoffs;
- predict direction and delay well enough to make an intentional choice;
- recognize how an operational incident connects to management and strategy;
- recover from an understandable failure without rote reloading; and
- distinguish purposeful management from repetitive maintenance.

Instrument descriptive events and state snapshots, but use observation and neutral interviews to
learn why players acted. Automated correctness checks and workload measurement are separate work;
player evidence does not replace them, nor they it.

## Deliver the design contract

Produce:

1. the managed subject, player role, experience hypotheses, constraints, and non-goals;
2. the causal system graph and simulation-fidelity budget;
3. the agent, aggregate, or hybrid decisions with their player-facing reasons;
4. operational, management, and strategic loop maps;
5. indirect-control contracts and exception paths;
6. crisis warning, intervention, consequence, recovery, and stopping-state designs;
7. world-signal, state, causal-trace, and forecast coverage for material outcomes;
8. automation boundaries and remaining decisions; and
9. prototype and playtest evidence, contradictions, and unresolved hypotheses.

The evidence and limitations behind these lessons are in
[sources.md](references/sources.md).
