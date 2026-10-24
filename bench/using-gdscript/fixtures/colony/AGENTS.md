# Colony

A colony simulation in Godot 4.7 and GDScript. `sim/` holds the simulation and touches no nodes;
`main.gd` drives it and shows it.

- Run the tests: `godot --headless --path . --script tests/run_tests.gd`.
- Time the tick: `godot --headless --path . --script tools/bench_tick.gd`.
