#!/bin/sh
# How we time logstat before a release.
set -e
[ -f access.log ] || cargo run --release --example gen -- 2000000 > access.log
time cargo run -q -- access.log > /dev/null
