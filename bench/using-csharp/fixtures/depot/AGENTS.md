# Transit

A delivery simulation: vans run routes between depots over track, and cars park at the kerb and cross
the track at level crossings. `src/Transit.Sim` is the simulation and references nothing else;
`game/` draws it and reads it only through `SimSnapshot` and the sim's public API.

- Build and test: `dotnet test`.
- The simulation is deterministic: no wall clock, no unseeded random numbers.
- Read a file before editing it; search before writing new logic.
- Make the smallest complete change. No option, wrapper, abstraction or "for later" code nobody asked
  for; deletion beats addition. Finish every caller and test the change breaks.
