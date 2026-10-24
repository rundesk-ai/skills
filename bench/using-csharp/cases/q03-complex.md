+++
skill = "using-csharp"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "tycoon"
rubric = """
result.1  Measures before changing anything: a timing of `Step` at a large business count, and allocation per tick (for example `GC.GetAllocatedBytesForCurrentThread`, or dotnet-counters), with the numbers reported.
result.2  Separates the causes: the unbounded `Log` list (memory that grows forever), per-tick allocation (LINQ `ToList`, closures, string interpolation, `new List`), and algorithmic cost (`Jobs.First(kv => kv.Value == job)` and `Businesses.Values.First(...)` are linear scans inside a loop, quadratic overall).
result.3  Fixes the quadratic lookups with direct indexing or a key carried with the job, bounds or removes the log, and reuses buffers instead of allocating per tick.
result.4  Keeps the simulation's results identical, proved by a digest or test comparing old and new behaviour over many ticks with the same seed, or states exactly which behaviour changed and why.
result.5  Adds a regression check for allocation or time that would fail if the per-tick allocation came back, and reports before and after numbers.
result.6  States what was not established: whether the stutter in the real client is GC pauses (which depends on the host's GC settings) and what remains unmeasured.
conduct.1 Takes numbers first and reports them; does not rewrite code on appearance alone.
"""
+++
With about 10,000 businesses the late game stutters every few seconds, and memory climbs the longer a
session runs. Make it smooth.
