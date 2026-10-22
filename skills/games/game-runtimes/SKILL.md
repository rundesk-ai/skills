---
name: game-runtimes
description: Use when designing, implementing, reviewing, or debugging engine-agnostic gameplay runtime architecture, including technical game loops, fixed-step simulation, input commands, update ordering, entity identity and mutation, gameplay events, deterministic replays, or save boundaries. It supplies timing and state-flow contracts that keep simulation reproducible and presentation responsive. Use the relevant language and engine skills alongside it; do not use it for player/core-loop design, the phase order and cadence of systems inside a world simulation's tick, general C++ ownership, profiling, or automated-test methodology alone.
---

# Engineer gameplay runtimes

Keep one authoritative simulation, make phase order explicit, and let rendering observe rather than
silently change the world.

## Establish the runtime contract

Before selecting a loop, record:

- whether play is continuous, turn-based, paused, slowed, or backgrounded;
- which host owns the application loop and which callbacks the game receives;
- monotonic wall time, simulation tick/time, presentation time, and each pause/time-scale policy;
- the systems that must run in strict order and structural changes they can request;
- whether replay, rollback, networking, or cross-run reproducibility is required; and
- the target platforms, refresh behavior, load spikes, and save/resume lifecycle.

Do not confuse this technical loop with the player's gameplay loop of decisions, actions, feedback,
and progression.

Profile to establish a frame budget, and use a debugging workflow for unexplained behavior: this
skill owns the intended timing and state contract, not reproduction, causal isolation, or fix proof.

## Drive one authoritative simulation

For continuous, timestep-sensitive authoritative simulation, default to this separation:

```text
pump host events -> sample/map input -> accumulate wall time
    -> run zero or more fixed simulation ticks (bounded)
    -> interpolate/present latest states -> audio/UI/output
```

Each simulation tick receives a constant `dt`, tick-stamped semantic commands, and owned deterministic
inputs. Keep previous and current presentation snapshots; render between them using the remaining
accumulator fraction. Never pass that remainder back as an odd-sized simulation step merely to catch
the display clock.

Keep presentation and other non-authoritative systems on their declared clocks when they do not need
the fixed simulation contract. Decide explicitly which state requires fixed stepping; do not force UI,
audio, animation, or event-driven work onto the tick merely because the world has one.

```text
Good: simulate fixed ticks; render lerp(previous, current, accumulator / tick_duration).
Bad:  integrate once with whatever duration the last frame happened to take.
```

Variable integration makes feel and stability depend on frame rate. A replay can record variable
durations, but that enlarges its input contract and still depends on controlled ordering, randomness,
floating-point behavior, and dependencies. A turn-based world may advance only on accepted actions,
while animation, audio, UI, and networking still need a nonblocking presentation/host loop.

Cap elapsed wall time admitted after a stall and cap simulation ticks per presentation frame. Choose
and document the overload behavior—temporary slowdown, dropped accumulated time, reduced workload, or
another product-specific policy. Unbounded catch-up can create a spiral in which late simulation asks
for ever more simulation.

Read [runtime contracts](references/runtime-contracts.md) when the task needs concrete pause and timer
policy, tick-command fields, input-buffer lifecycle, phase and mutation rules, stable identity, event
ordering, replay envelopes, or save/load and storage behavior. Those detailed contracts live only in
that reference.

## Define authoritative data flow

Map devices to semantic actions at the adapter boundary and assign accepted inputs to simulation
commands; device callbacks do not mutate gameplay. Write the system phases and structural commit as
an explicit order. Resolve durable gameplay facts before presentation, audio, UI, achievements, or
telemetry consumes them.

Use stable domain identity across phases and adapters. Pointer, iterator, container, and ownership
mechanics belong to the language's own guidance; this skill owns when the game resolves a handle,
commits lifecycle changes, and exposes the result.

```text
Good: input -> tick command -> authoritative result -> committed event -> presentation.
Bad:  device, physics, or animation callbacks each mutate the same world immediately.
```

## Make reproducibility and persistence bounded claims

Keep saves distinct from replay logs, and declare the envelope each one promises. A fixed tick is a
strong default for continuous action simulation, not a universal replay prerequisite. The replay
envelope, capture list, and save boundary are in [runtime contracts](references/runtime-contracts.md).

Prove the architecture with engine-free simulation cases, frame-rate variation, long-frame overload,
pause/resume, command replay, stale identities, structural changes during update, save/load round
trips, and the actual engine adapter.

Read [the source map](references/sources.md) when auditing or changing these rules.
