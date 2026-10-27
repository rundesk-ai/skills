# Grid

A city road simulation: roads in classes, buildings with entrances, traffic speeds per road, and the
build tool and map that show them. `src/Grid.Sim` is the simulation and references nothing else;
`game/` draws it and holds the tools, and reads the simulation through `SimSnapshot` and its public API.

- Build: `dotnet build`.
- The simulation steps on its own thread; the game reads only the snapshot it publishes.
