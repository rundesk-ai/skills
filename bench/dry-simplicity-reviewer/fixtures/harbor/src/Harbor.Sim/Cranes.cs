namespace Harbor.Sim;

/// <summary>Figures every quay crane shares.</summary>
public static class CraneSpec
{
    /// <summary>Trolley speed along the boom, metres per second.</summary>
    public const float TrolleySpeed = 3f;

    /// <summary>Seconds to lock or release the spreader on a container.</summary>
    public const float LockSeconds = 0.5f;
}

/// <summary>The quay cranes: which ship each works, and when it is free again.</summary>
public sealed class CraneSystem
{
    private readonly List<int> _ship = [];
    private readonly List<long> _busyUntil = [];
    private readonly List<float> _boomAt = [];

    /// <summary>Raised when a crane has no ship left to work.</summary>
    public event Action<int>? Idle;

    /// <summary>Scales every move: above 1 for faster cranes.</summary>
    public float SpeedFactor { get; set; } = 1f;

    /// <summary>When set, decides for a crane whether it skips its turn.</summary>
    internal Func<int, bool>? PickOverride { get; set; }

    public int Count => _ship.Count;

    public int Add(float boomAt)
    {
        _ship.Add(-1);
        _busyUntil.Add(0);
        _boomAt.Add(boomAt);
        return _ship.Count - 1;
    }

    public void Assign(int crane, int ship) => _ship[crane] = ship;

    public long BusyUntil(int crane) => _busyUntil[crane];

    public void Step(long tick, Fleet fleet)
    {
        for (var c = 0; c < _ship.Count; c++)
        {
            if (PickOverride?.Invoke(c) == true || tick < _busyUntil[c] || _ship[c] < 0)
                continue;
            var ship = fleet.Ships[_ship[c]];
            var fore = c % 2 == 0;
            var container = fore ? Fleet.UnloadFore(ship) : Fleet.UnloadAft(ship);
            if (container < 0)
            {
                _ship[c] = -1;
                Idle?.Invoke(c);
                continue;
            }

            var distance = MathF.Abs(_boomAt[c] - (fore ? 0f : ship.Length));
            var seconds = ((distance / CraneSpec.TrolleySpeed) + (2f * CraneSpec.LockSeconds)) / SpeedFactor;
            _busyUntil[c] = tick + Clock.Ticks(seconds);
        }
    }

    /// <summary>When crane <paramref name="crane"/> will have cleared <paramref name="containers"/> more boxes from its stack.</summary>
    public long EstimateFinish(int crane, int containers, float shipLength, long now)
    {
        var distance = MathF.Abs(_boomAt[crane] - (crane % 2 == 0 ? 0f : shipLength));
        var seconds = ((distance / CraneSpec.TrolleySpeed) + (2f * CraneSpec.LockSeconds)) / SpeedFactor;
        return Math.Max(now, _busyUntil[crane]) + (containers * Clock.Ticks(seconds));
    }
}
