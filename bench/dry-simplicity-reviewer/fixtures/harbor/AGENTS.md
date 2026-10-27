# Harbor

A port simulation: ships arrive on the tide, are planned onto berths, and quay cranes unload them.
`src/Harbor.Sim` is the simulation and references nothing else; `game/` draws it through the sim's
public API. `data/events.json` schedules weather events by handler name.

- Build and test: `dotnet test`.
- The simulation is deterministic: no wall clock, no unseeded random numbers.
