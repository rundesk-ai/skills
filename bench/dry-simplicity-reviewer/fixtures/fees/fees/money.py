def percent_of(cents: int, basis_points: int) -> int:
    """`basis_points` hundredths of a percent of `cents`, rounded half up. Amounts are never negative."""
    return (cents * basis_points + 5_000) // 10_000
