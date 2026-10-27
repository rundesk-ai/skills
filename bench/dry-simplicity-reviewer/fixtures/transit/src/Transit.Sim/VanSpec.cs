namespace Transit.Sim;

/// <summary>Figures every delivery van shares.</summary>
public static class VanSpec
{
    /// <summary>Top speed, metres per second.</summary>
    public const float MaxSpeed = 16f;

    /// <summary>Service braking, metres per second squared.</summary>
    public const float Braking = 1.2f;

    /// <summary>Seconds a freight van stands at a depot.</summary>
    public const float FreightDwell = 40f;
}

/// <summary>The simulation's clock.</summary>
public static class Clock
{
    public const int TicksPerSecond = 20;
}
