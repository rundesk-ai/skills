# Settlement

A settlement simulation in plain Python 3, standard library only: workers chop trees and eat. `sim/`
holds the simulation; there is no renderer.

- Run the tests: `python3 -m unittest discover -s tests -t .`
- Run a large settlement and print its numbers: `python3 -m tools.bench_tick 300`
