# Traps

Read this when an agent-behaviour symptom has no obvious cause. Each entry gives the symptom, its cause,
the replacement, and the proof that it is fixed.

| Symptom | Cause | Replacement | Proof |
|---|---|---|---|
| Agent flips between two actions and finishes neither | Near-equal scores re-evaluated each tick | A consideration that separates them; expiring commitment bonus; cooldown; decide when the queue empties | Equal-score fixture: ≤1 switch per game hour, counted in the trace |
| Agent lies down and gets up repeatedly; flees and returns | One threshold for entering and leaving | Deadband plus re-entry lockout; an explicit exit rule for fleeing | Need held just under threshold gives one transition |
| A worse option nearby beats a better one far away | Distance folded into utility | Rank or tier first; distance only breaks ties within a class | Far high-value vs near low-value fixture picks the far one |
| Agents always pick the action with metres or hit points as input | Unnormalised inputs added or multiplied | Bounds, 0–1, curves; or fixed score bands | Every logged component lies in 0–1; sensitivity sweep per input |
| Carefully specified options never win | Product of many terms below 1 | Compensation for consideration count | Equal per-term scores, different counts, score within ε |
| Five workers walk to one target; four turn back | No claim at selection | Claim before travel, with a maximum number of claimants | 10 agents, 3 jobs, one tick: ≤3 claimants, no turn-backs |
| Agents idle beside available work | Claims released on some exit paths only | Release in cleanup for every outcome; release-all on death; lease and sweep | Invariant each tick: every holder alive with a current job; random kill and interrupt fuzz |
| One haul blocks a whole container | Whole-object lock | Count claims; maximum claimants | Two haulers of 25 from a stack of 50 both succeed |
| Long action never progresses; its start animation replays | Memoryless re-traversal re-initialises the running leaf | Stateful tick wrapper; sequence with memory; reactive checks only in chosen parents | A 600-tick action is initialised exactly once |
| Interrupted agent keeps a claim, path request or carried item | Higher branch never aborts the old one | Parent aborts the loser, whose terminate cleans up | Interrupt at every step index; nothing left held |
| Agent keeps working while on fire | Non-reactive selector resumes the running child without rechecking | Reactive selector or observer-abort decorator | Condition raised mid-action switches within one decision interval |
| Fleeing agent runs back into danger, then flees again | Stateless behaviours with no memory | Explicit memory fields gating re-entry | No re-entry before memory expires |
| Frame spikes every N ticks; crowds change activity in lockstep | Everyone thinks on the same tick; schedules switch at one hour | Hashed phase; staggered system passes; per-agent schedule jitter; small reaction delays | Decisions-per-tick histogram: max/mean below a set ratio |
| Agents die of thirst beside water under load | Need damage runs on its own clock; the satisfying decision waits for a budget slot | Lethal band bypasses the budget, or grace while a satisfy job is queued | Maximum-population soak: zero deaths near an unclaimed source |
| Low-priority work never happens, or agents trek across the map | Strict tiers without ageing; locality limits without escape | Ageing exception for old jobs; a dedicated labour pool; player-visible priority | Age of the oldest open job per tier stays bounded |
| Agent starts and abandons jobs every tick | Validity check and job creation disagree, or target invalid at start | Make both use one predicate; a thrash tripwire with recovery and a brief blacklist | Forced-mismatch fixture: tripwire fires once, agent recovers |
| Agent repeats one action forever | An object advertises a reward it does not grant | Rewards granted inside the action; forced actions pushed on the queue | Advertised and observed need change agree within ε |
| A planner repeats the same combo every time | The executing task's own effect triggers a replan | Model the missing fact; do not treat own effects as sensor changes | No replan with cause "own effect" in the trace |
| A replan cuts a still-valid task short | Any replan replaces the plan | Accept a new plan only if its method priority is equal or higher | Irrelevant fact changed mid-task: task not aborted |
| Replays diverge; behaviour differs between builds | Ties by container or pointer order; hash-map iteration; global random draws | Total-order comparators ending in ids; ordered containers; seeded per-agent streams | Same seed, different iteration orders: identical hashes of job board and claims |
| Off-screen agents starve faster, or never | Decision frequency or existence tied to visibility | Fidelity may lower cadence but must keep outcomes; presentation LOD separate | Same seed, camera parked elsewhere: identical outcome hashes |
| A new need stops agents eating | Priorities spread across composed state machines | One arbitration point; behaviours below it only execute | Regression fixture per lethal need, run when a need is added |
| Players cannot predict agents | Rich hidden state at a scale nobody inspects | Simulate only what the player sees or one layer below; reason codes for every decision | Every decision has a player-readable reason |
| Endless "cannot reach" cancellations | Jobs posted without a reachability test | Component-id comparison before posting or claiming | No posted job targets a component no eligible worker is in |
