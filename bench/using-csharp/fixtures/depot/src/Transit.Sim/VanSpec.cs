namespace Transit.Sim;

/// <summary>Figures every delivery van shares.</summary>
public static class VanSpec
{
    /// <summary>Top speed, metres per second.</summary>
    public const float MaxSpeed = 16f;

    /// <summary>Service braking, metres per second squared.</summary>
    public const float Braking = 1.2f;

    /// <summary>How far a van at top speed runs braking to a stand, metres.</summary>
    public const float BrakingDistance = MaxSpeed * MaxSpeed / (2f * Braking);

    /// <summary>Seconds a freight van stands at a depot.</summary>
    public const float FreightDwell = 40f;

    /// <summary>Seconds a van that cannot move waits before it tries again.</summary>
    public const float RetrySeconds = 5f;
}

/// <summary>The simulation's clock.</summary>
public static class Clock
{
    public const int TicksPerSecond = 20;

    /// <summary>The ticks in <paramref name="seconds"/>, rounded down.</summary>
    public static long Ticks(float seconds) => (long)(seconds * TicksPerSecond);
}
