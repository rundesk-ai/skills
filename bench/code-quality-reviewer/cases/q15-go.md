+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
trap = "language traps whose answer depends on the version pinned in go.mod, not the toolchain on the machine"
fixture = "ingest"
cases_version = 2
key = """
go.mod pins go 1.21, and AGENTS.md says why. Under 1.21 semantics a loop variable is shared across iterations; a reviewer that assumes Go 1.22+ per-iteration variables misses M1.
must:
  M1 bug       SumAll starts a goroutine per path whose closure captures the loop variable p; under go 1.21 every goroutine shares one p, so 50 files produced 50 results for 1 distinct path (reproduced), and the other 49 files are never read. Fix: pass p as an argument, as Largest does with r, or shadow it (p := p). Credit needs the go.mod version as the reason; "loop variable capture" without it is still a hit if the mechanism is right.
  M2 bug       CountLines defers f.Close() inside the loop, so every file stays open until the function returns: 50 descriptors were open while it read the 51st (reproduced). Over a night's tens of thousands of files it fails with "too many open files". Fix: close each file at the end of its iteration, or move the body into a function.
  M3 bug+rule  SumFile declares v, err := strconv.Atoi(line) inside the loop, shadowing the named result err; a corrupt line breaks out and the function returns the partial total with a nil error ("10 20 ERR 30" gives 30, nil; reproduced). Breaks "A file that cannot be read in full is reported as an error". Fix: return 0 and the error (with the line) at the failure.
good code:
  G1 Largest passes r into the goroutine and guards best/bestTotal with a mutex; correct (its goroutines add nothing for a CPU-trivial comparison, which is taste, see T1).
  G2 results channel buffered to len(paths), closed after wg.Wait(): no goroutine blocks; correct.
decoys:
  D1 defer mu.Unlock() inside Largest's goroutine: runs when each goroutine returns; correct, unlike M2.
  D2 the tie-break r.Path < best in Largest: deterministic by design.
taste:
  T1 goroutines in Largest are unnecessary for a comparison; T2 strings.Split on the whole file rather than a Scanner; T3 named results.
extras:
  X1 SumFile reads the whole file into memory; a Scanner would stream it.
  X2 SumAll starts one goroutine per file with no limit on how many run at once (tens of thousands at night).
"""
+++
Review this Go module for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
