# logstat

Per-endpoint request counts, 5xx errors, bytes and p95 latency from the gateway's access log. The
nightly job runs it over the day's log (about 40 million lines) and it has become the slowest step.

`./bench.sh` generates a 2-million-line sample log and times a run.
