# Transit

A delivery simulation: vans run routes between depots over track, and cars park at the kerb and cross
the track at level crossings. `src/Transit.Sim` is the simulation and references nothing else;
`game/` draws it and reads it only through `SimSnapshot` and the sim's public API.

- Build and test: `dotnet test`.
- The simulation is deterministic: no wall clock, no unseeded random numbers.
