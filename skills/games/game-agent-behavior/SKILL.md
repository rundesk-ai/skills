---
name: game-agent-behavior
description: Use when designing, implementing, tuning, reviewing, or debugging how game or simulation agents decide what to do (colonists, citizens, workers, animals, NPCs), including state machines, behavior trees, utility AI, GOAP or HTN planners, needs, daily schedules, job and work assignment, reservations, interruptions, decision cadence, or agents that dither, stampede one job, idle beside work, starve under load, or spike the frame by the thousand. It supplies the architecture choice, a think/act split, claim and release rules, staggered budgets, and decision traces with proof fixtures. Do not use it for route search and movement, or for deciding what a management game should let the player control.
---

# Engineer agent behavior

Agent decision bugs are rarely about the architecture's name. They come from deciding too often, from
two agents believing they own the same thing, from claims that are never released, and from choices
nobody can explain afterwards. Build the skeleton that prevents those first, then choose how options
are scored.

## Split thinking from acting

The decision layer emits one bounded task, or a short queue of actions. A separate executor runs each
action through `start`, `tick`, `finish` and `abort`, and `abort` always cleans up. Decide again only
when the queue empties, when an interrupt fires, or on a slow periodic check.

Shipped examples follow this shape. F.E.A.R. kept a three-state machine and put every choice in a
planner. A tower sim ran 1,000 NPCs at 60 FPS by re-selecting only when an NPC's action queue was
empty. A city builder's developer, having spread decisions across agent code, a global work list and
building state machines, named that spread as the source of the game's bugs: adding a new need broke
old behaviour. Keep one arbitration point per agent; everything below it only executes.

Deviate only for twitch combat that must re-evaluate every update, and even then suspend evaluation
once an ability has committed.

## Decide what agents choose and what a coordinator owns

Agents choose among valid options: which meal, which bed, which ordinary job. Scarce targets,
exclusive claims and emergency priority belong to a coordinator that makes claims atomically. If jobs
pick workers, the nearest qualified worker gets snatched; if workers pick jobs, they take work another
would do better. Dwarf Fortress runs job assignment every 100 ticks, with job applications staggered
from it. With few agents and few jobs, idle agents pulling from a job board is enough.

## Choose the architecture from the decision's shape

When unsure, start with an ordered list of threshold-gated options and an action queue. That is what
most shipped colony sims do; add scoring when ordering stops expressing the design.

| Situation | Default | Failure to design against |
|---|---|---|
| Few modes, clear transitions (animal, door, vehicle) | State machine, hierarchical once states pass a dozen; reset in enter and exit | Transition explosion; state that survives across visits |
| Workers choosing among job categories | Ordered tiers: scan tiers in order, take the nearest valid target in the first tier that yields; needs as top tiers | Low tiers starving; no notion of efficiency |
| Many needs and objects, no single right answer | Utility over what objects advertise, scored by the need relief they give | Dithering; distance inside the score; false advertising |
| Authored multi-step behaviour with interrupts | Behavior tree with stateful nodes, reactive or observer-abort conditions | Restarting the running action every tick; no cleanup on abort |
| Hard priorities plus soft preference | Dual utility: rank buckets first, weighted random among the near-best of the top rank | Too many ranks, which become a hidden priority list |
| Goals reachable by different action sets per agent type | Goal planner (A* over a fixed world-state array), plans of a few actions, replanned rarely | Lost authorial control; cost grows with branching |
| Designer-ordered methods with fallbacks | Hierarchical task network, total-order decomposition | Replanning on the task's own effects; aborting a still-valid task |
| Background population's day | Schedule keyed by time that sets thresholds; the agent asks it when idle | Crowds switching activity on the same tick |
| Scenes needing several agents (meal, conversation) | Smart object with role slots, reserved when committed | Two scenes on one prop; a role leaving mid-scene |

## Score options so they compare

- Normalise every input to 0–1 between explicit bounds, then apply a response curve. Raw metres or hit
  points multiplied by weights let one input dominate everything.
- Multiply considerations, with zero as a veto, and order them cheapest first: line of sight and path
  queries last. Compensate for the number of considerations. Twenty-five terms of 0.9 multiply to
  0.07, so a carefully specified option otherwise loses to a crude one. Compare like with like in any
  "cannot win" early-out.
- Score need relief, not need level: the attenuated difference a curve gives between current and
  satisfied. Raw sums make a hunger change from 70 to 90 count the same as thirst from 10 to 30.
- Let tier or rank decide first and distance only break ties within a class. Folding distance into
  utility makes a worse action nearby beat a better one far away.
- Break ties with a total order ending in stable ids. Draw any randomness from a seeded per-agent
  stream, after dropping zero-weight and far-below-best options.

Read [patterns](references/patterns.md) for the code: the utility selector, a behavior-tree tick with
correct running and abort semantics, the job board with reservations, staggered cadence, the action
lifecycle and the decision trace.

## Stop dithering with hysteresis and memory

An agent flipping between two near-equal options every few ticks finishes neither. In order of
preference: add a consideration so that one option wins consistently; give the current choice a bonus
that expires; add a cooldown; decide only when the queue empties. A bonus moves where the scores land
and does not remove oscillation on its own, so test with options tuned to equal scores.

Give every threshold a deadband: act when a need falls below one level, stop above a higher one, and
lock out re-entry for a while. A single threshold for entering and leaving makes agents lie down and get
up repeatedly. Store memory explicitly (`fledUntilTick`, `lastThreatPos`). A stateless tree otherwise
loops a fleeing citizen back into the battle it fled.

## Claim at selection; release on every exit

- Reserve the target when the job is chosen, before travel, with the claimant's id. Setting a flag on
  arrival sends five workers to one tree and four of them back.
- Reserve counts, not whole objects: two haulers taking 25 each from a stack of 50 must both succeed.
  Allow a maximum number of claimants for shared work.
- Release in the action's cleanup path for every outcome, and release everything a claimant holds when
  it dies, despawns or changes side. Releasing only on success leaks claims, and agents then idle
  beside available work.
- Check reachability with a component-id comparison before posting or claiming a job. Otherwise the
  generator emits jobs nobody can do, and agents cancel them forever.
- Give claims a lease renewed by progress, with a sweep that logs and removes expired ones. That turns
  a leak into a bounded delay you can see. No source shows a shipped lease, so treat this as a safety
  net, not a substitute for structural release.

Generate jobs from events (an ingredient arrives, a blueprint is placed) and keep a slow, rotating,
work-counted sweep that re-finds anything an event missed. On failure, flush the queue and select
again. Leave intermediate results in the world for a later pickup rather than resuming
half-finished work.

## Schedule thinking; never think everyone every tick

- Run a periodic check per agent at a phase taken from a hash of its id, so the population spreads
  evenly over the interval. `tick % N == 0` for everyone spikes every N ticks.
- Wake agents by event: a target destroyed, a job posted, damage taken. Put timed wakes (a need crossing
  its threshold, a cooldown ending) in a min-heap keyed by tick, computed from the decay rate rather
  than polled.
- Count decision budgets in decisions per tick, never in milliseconds, so replays do not depend on
  machine speed. Serve dirty agents in id order from a rotating start, so nobody starves.
- A crossing into a lethal band forces a decision that bypasses the budget. One colony sim's animals
  died of thirst beside water because "the AI slicer cannot keep up".
- Jitter schedule boundaries per agent, deterministically, so a town does not change activity in one
  tick.
- Lower decision frequency with distance or importance if needed, but never change outcomes. Agents
  must not starve faster, or never, depending on where the camera is.

Read [scale and proof](references/scale-and-proof.md) for the counters, the reported cadences and agent
counts, and the order to try optimisations.

## Make every decision explainable

Keep a bounded ring buffer of decisions per agent. Each entry holds the tick, the trigger, the chosen
option with its score and per-consideration components, the top runners-up, the rejected options with a
stable reason code (filtered, unreachable, reserved by an id, vetoed by a consideration, lower rank),
held claims, and the commitment window. Generate player-facing explanations from those codes, never from
stored prose. Designers debugging a utility system and players reading a colonist's thought both depend
on it.

## Prove it

- Two-agent fixtures reproduce most behaviour bugs. Use headless tests that wait until a condition
  holds within N ticks, so a stuck agent fails the test instead of hanging it.
- Ten agents and three jobs in one tick give at most three claimants and no turn-backs.
- Kill or interrupt agents at random ticks: every claim's holder is alive and its job is current, and
  no agent ends holding an item or claim from an aborted action.
- Options tuned to equal scores switch at most once per game hour.
- A 600-tick action is initialised once.
- At maximum population, no agent dies of a need within reach of an unclaimed source. The age of the
  oldest open job per tier stays bounded.
- The same seed with a different iteration order, a different camera position and a different thread
  count gives identical per-tick hashes of the job board and claim table, not only of positions.
- Add a thrash tripwire. An agent starting and abandoning jobs many times within a few ticks logs its job
  list, enters a recovery wait, and briefly blacklists the target.

Read [traps](references/traps.md) when a symptom matches and the cause is not obvious. Read
[the source map](references/sources.md) to audit or change these rules.
