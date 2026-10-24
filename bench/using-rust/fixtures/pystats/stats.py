"""Batch summary for the nightly reporting job.

Uses the compiled fastagg extension when it is installed, and this pure-Python fallback otherwise.
"""


def summarize(values):
    total = sum(values)
    return {
        "count": len(values),
        "total": total,
        "mean": total / len(values),
        "max": max(values),
    }
