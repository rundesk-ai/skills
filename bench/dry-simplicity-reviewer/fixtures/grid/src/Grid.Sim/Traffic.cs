namespace Grid.Sim;

/// <summary>Where a road's speed ratio (driven speed over its limit) crosses from one traffic band into the next.</summary>
public static class Congestion
{
    public const float FreeAbove = 0.8f;
    public const float SlowAbove = 0.6f;
    public const float HeavyAbove = 0.4f;
}

/// <summary>What the game reads each frame, copied so the game thread never reads arrays the simulation is stepping.</summary>
public sealed record SimSnapshot(long Tick, IReadOnlyDictionary<int, float> SpeedRatios, int RoadCount);

/// <summary>The simulation: the network, the buildings and each road's speed ratio.</summary>
public sealed class Simulation
{
    private readonly Dictionary<int, float> _ratios = [];

    public Network Network { get; } = new();

    public List<Building> Buildings { get; } = [];

    public long Tick { get; private set; }

    public void Step()
    {
        Tick++;
        foreach (var road in Network.Roads)
            _ratios[road.Id] = 1f - (0.1f * (road.Id % 7));
        foreach (var building in Buildings.Where(b => b.Entrance < 0))
            Entrances.Connect(Network, building);
    }

    public SimSnapshot Publish() => new(Tick, new Dictionary<int, float>(_ratios), Network.Roads.Count());
}
