"""Integer-cent money helpers. Amounts are never negative here: refunds live elsewhere."""


def cents_to_str(cents: int) -> str:
    return f"${cents // 100:,}.{cents % 100:02d}"


def percent_of(cents: int, basis_points: int) -> int:
    """`basis_points` hundredths of a percent of `cents`, rounded half up."""
    return (cents * basis_points + 5_000) // 10_000
