"""Raise the patch number in VERSION. Used by `make release` only."""
major, minor, patch = open("VERSION").read().strip().split(".")
open("VERSION", "w").write(f"{major}.{minor}.{int(patch) + 1}\n")
