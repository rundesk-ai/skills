# AGENTS

`ingest` reads the meter-reading files that sensors upload each night and totals them per file.
Go, standard library only. A night brings tens of thousands of files. `go.mod` pins `go 1.21`
because the build servers still run Go 1.21; do not raise it.

## Rules

- **A file that cannot be read in full is reported as an error**, never as a smaller total.

## Build, test & run

```sh
go test ./...
```
