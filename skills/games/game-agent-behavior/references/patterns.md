# Decision patterns

Read this before writing or reviewing a selector, a behavior-tree runtime, a job board, a think
scheduler, an action executor or a decision trace. The pseudocode is language-neutral. `tick` is the
integer simulation tick, `id` is a stable integer entity id, and every comparator ends with ids, so that
ordering is total.

## Utility selector: bounds, curves, compensation, rank and hysteresis

```text
struct Consideration { input: fn(agent, target) -> number; lo, hi; curve }   # linear | power | logistic | piecewise
fn score01(c, a, t):
    x = clamp((c.input(a, t) - c.lo) / (c.hi - c.lo), 0, 1)   # normalise BEFORE the curve
    return clamp(c.curve(x), 0, 1)

struct Option { id, rank: int, weight, considerations }       # considerations ordered cheapest first

fn compensate(s, n, w):            # offsets the penalty of multiplying many terms below 1
    if n == 0 or s == 0: return s
    makeUp = (w - s) * (w - w / n)
    return s + makeUp * s

fn evaluate(opt, a, t, bestSoFar):
    s = opt.weight * (opt.id == a.current.optionId ? a.momentum : 1)   # expiring commitment bonus
    n = len(opt.considerations)
    for c in opt.considerations:
        s *= score01(c, a, t)
        if s == 0: return 0                                     # veto
        if compensate(s, n, opt.weight) < bestSoFar: return 0   # cannot win: compare like with like
    return compensate(s, n, opt.weight)

fn choose(a):
    cands = [(o, t) for o in a.options for t in targetsFor(o, a) if passesFilters(o, t)]
    topRank = max(o.rank for (o, t) in cands if evaluate(o, a, t, 0) > 0)       # rank first
    best = none
    for (o, t) in cands where o.rank == topRank, in (o.id, t.id) order:
        s = evaluate(o, a, t, best ? best.score : 0)
        if s > 0 and (best == none or (s, -dist(a, t), -o.id, -t.id) > best.key): best = ...
    if a.current and best.option != a.current.option and tick < a.commitUntil
       and best.score < scoreOf(a.current) * (1 + SWITCH_MARGIN):
        return a.current                                        # hysteresis
    trace(a, cands, best)
    return best
```

- A multiplied score can only fall as terms are added, so evaluating the compensated value of a partial
  score is an optimistic bound for the "cannot win" check. One open-source implementation compares
  the uncompensated partial score with a compensated best, which can prune an option that would have
  won.
- To pick weighted-randomly instead of the single best, drop zero weights, keep the top rank, drop
  options far below the best, then draw from a seeded per-agent stream. A global random draw both picks
  visibly stupid options and desynchronises replays.

```text
BAD   score = hunger + thirst + fun                 # raw levels: 70->90 hunger equals 10->30 thirst
GOOD  score = Σ A(cur_i) - A(cur_i + delta_i)       # relief through a non-increasing attenuation curve

BAD   score = utility / distance²                   # a worse action nearby beats a better one far away
GOOD  rank decides first; distance only breaks ties inside one class

BAD   rawMetres * w1 + hitPoints * w2               # one unnormalised input dominates
GOOD  bounds -> 0..1 -> curve, or fixed designer score bands per behaviour class
```

## Behavior-tree tick with running and abort semantics

```text
enum Status { INVALID, RUNNING, SUCCESS, FAILURE, ABORTED }

class Node:
    status = INVALID
    fn tick(ctx):                                   # the only entry point
        if status != RUNNING: onInitialize(ctx)     # once, before the first update
        status = update(ctx)
        if status != RUNNING: onTerminate(ctx, status)
        return status
    fn abort(ctx):                                  # a parent pre-empts a running child
        if status == RUNNING: onTerminate(ctx, ABORTED); status = ABORTED
    # a leaf never blocks in update(); onTerminate releases claims and cancels path requests

class Sequence(children):                           # with memory: resume the running child
    i = 0
    onInitialize: i = 0
    update(ctx):
        while i < len(children):
            s = children[i].tick(ctx)
            if s != SUCCESS: return s
            i += 1
        return SUCCESS

class ReactiveSelector(children):                   # re-checks higher priorities every tick
    running = none
    update(ctx):
        for c in children:
            s = c.tick(ctx)
            if s != FAILURE:
                if running != none and running != c: running.abort(ctx)   # always abort the loser
                running = (s == RUNNING) ? c : none
                return s
        return FAILURE
    onTerminate(ctx, st): if running != none: running.abort(ctx)
```

```text
BAD   every tick: walk from the root and call start() on the first action whose condition holds
      # re-initialises a 600-tick build every tick, or switches actions without stopping the old one
GOOD  resume RUNNING children; put interrupting conditions in a reactive parent or an observer-abort
      decorator; the parent aborts the loser, so its onTerminate(ABORTED) cleans up

BAD   release the reservation in the SUCCESS branch of update()
GOOD  release in onTerminate for any status, and in release-all-by-claimant on death
```

Libraries name the same contract differently: a running action has `onStart`, `onRunning` and
`onHalted`, and a halted one must stop as fast as possible. A reactive sequence restarts from its first
child every tick and halts the running action when a condition fails, while a plain sequence re-ticks
only the running child. Engine trees attach conditions as decorators that abort lower-priority or own
branches when an observed key changes. For thousands of agents, keep the tree structure shared and
per-agent task state separate. Let a leaf waiting on another system suspend until a callback wakes it,
instead of re-traversing.

## Job board with tiers and count reservations

```text
struct Claim { claimant, job, target, maxClaimants, count, expiresTick }
index byTarget, byClaimant                       # not one flat list scanned per query

fn canClaim(c, target, maxClaimants, count):
    rs = byTarget[target] excluding c and expired
    if len(rs) >= maxClaimants: return false
    if count != ALL and sum(r.count for r in rs) + count > available(target): return false
    return true

fn findJob(a):
    for tier in a.tiersInPriorityOrder:          # needs and emergencies are earlier tiers
        best = none
        for giver in tier.givers:
            for t in giver.candidates(a):        # spatial index or per-region list, not a world scan
                if not giver.valid(a, t) or not reachable(a, t): continue      # reachability before claim
                if not canClaim(a, t, giver.maxClaimants, giver.count): continue
                best = minBy(best, (giver, t), key = (dist2(a, t), t.id))
        if best: return best.giver.makeJobAndClaim(a, best.t)   # claim BEFORE travel
    return none

fn releaseAllForJob(job)                         # from action cleanup, every outcome
fn releaseAllClaimedBy(c)                        # on death, despawn, change of side
fn sweepExpired(budget):                         # rotating cursor, work-counted
    repeat budget times: r = nextInRotation(); if r.expiresTick < tick: log(LEAK, r); remove(r)
```

```text
BAD   target.isTaken = true on arrival, cleared on success
      # N agents pick the same nearest target; N-1 arrive to find it taken; a death leaves it taken forever
GOOD  claim at selection with the claimant id; release on every exit path; lease and sweep as a net

BAD   lock a whole container while one item is hauled
GOOD  claim a count of its capacity
```

## Staggered cadence, event wakes and a count budget

```text
INTERVAL = 30
fn phase(id) = hash32(id ^ SALT) % INTERVAL      # deterministic stagger, no random draw

wakeHeap: min-heap of (wakeTick, id)             # threshold crossings, cooldowns, schedule changes
dirty: ordered set of id                         # event wakes: target gone, job posted, damage

fn simTick():
    while wakeHeap.top.wakeTick <= tick: dirty.add(wakeHeap.pop().id)
    for a where (tick + phase(a.id)) % INTERVAL == 0: dirty.add(a.id)
    budget = MAX_DECISIONS_PER_TICK              # decisions, never milliseconds
    for id in dirty, ascending from a rotating start:
        if budget == 0 and not lethal(agent(id)): continue   # lethal bands bypass the budget
        think(agent(id)); budget -= 1; dirty.remove(id)
    for a in activeExecutors: a.executor.tick()  # acting runs every tick and is cheap

fn onNeedChanged(a, need):
    wakeHeap.push(tick + ticksUntil(need, need.urgentThreshold), a.id)   # from the decay rate
```

```text
BAD   for a in agents: a.think()                       # everyone, every tick
BAD   if tick % 30 == 0: for a in agents: a.think()    # everyone on the same tick: a spike every 30
BAD   while elapsedMs() < 2: think(next())             # replay depends on machine speed
GOOD  hashed phase + event wakes + count budget + rotating start + lethal bypass
```

Time-slicing removes spikes; it does not make the frame cheaper on average. Printed time-slicing
listings in at least one published chapter contain bugs, so write the scheduler from the contract above
and test it.

## Action lifecycle on the executor side

```text
interface Action { start(a) -> Status; tick(a) -> Status; finish(a); abort(a, reason) }
struct ActionInstance { def, target, job, failOn: [predicate], startedTick, maxTicks }

fn executorTick(a):
    act = a.queue.front
    for p in act.failOn: if p(a): return fail(a, act, p.code)     # TARGET_GONE, UNREACHABLE, ...
    if tick - act.startedTick > act.maxTicks: return fail(a, act, TIMEOUT)
    if act.def.tick(a) == SUCCESS: act.def.finish(a); grantReward(a, act); a.queue.pop()

fn fail(a, act, code):
    act.def.abort(a, code); releaseAllForJob(act.job)
    a.queue.clear(); pushFallback(a, code)                        # flush, then select again
    trace(a, FAIL, code)
```

The action grants its own reward, so an interrupted action is not rewarded. An object that advertises a
reward it does not grant creates loops that are very hard to tune.

## Decision trace

```text
struct DecisionTrace {                     # ring buffer per agent, e.g. the last 16
    tick, agent, trigger: QUEUE_EMPTY | INTERRUPT(code) | PERIODIC | FORCED
    chosen: { option, target, score, rank }
    components: [ { consideration, raw, normalised, curved } ]      # for the chosen option
    runnersUp: top 3 { option, target, score }
    rejected: bounded [ { option, target, reason: FILTERED | UNREACHABLE | RESERVED_BY(id)
                          | VETO(consideration) | LOWER_RANK | BELOW_CUTOFF } ]
    claimsHeld, commitUntil, hysteresisApplied
}
```

Record after the simulation step, in fixed memory. Show it in a debug table per agent, and generate a
player's "why" text from the reason codes.
