# Town

Road traffic for a grid town in plain Python 3, standard library only. `sim/` holds the simulation;
there is no renderer.

- Run the tests: `python3 -m unittest discover -s tests -t .`
- Run rush hour and print its numbers: `python3 -m tools.bench_tick 3 1` (cars spawned per tick, game
  speed).
