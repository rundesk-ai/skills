# Tycoon

A business tycoon simulation. `src/Tycoon.Sim` is the simulation and references no engine; the game
client loads it as a library. Replays and saves must reproduce the same game.

- Build and test: `dotnet test`.
- Keep `Tycoon.Sim` free of engine and UI types.
