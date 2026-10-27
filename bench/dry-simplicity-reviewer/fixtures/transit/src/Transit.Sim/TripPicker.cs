namespace Transit.Sim;

/// <summary>A place cars enter or leave the map, and how many cars a minute its lanes carry.</summary>
public sealed record Gate(int CarsPerMinute, bool Inbound);

/// <summary>Draws where through trips come from and go to.</summary>
public sealed class TripPicker(SimRandom random)
{
    /// <summary>Whether each inbound gate reaches any outbound one.</summary>
    public bool[] ReachesAny { get; set; } = [];

    /// <summary>Whether gate i reaches gate j, at [i * n + j].</summary>
    public bool[] Reach { get; set; } = [];

    /// <summary>Extra weight on every draw, for events such as a rush hour.</summary>
    public int Boost { get; private set; } = 1;

    public void SetBoost(int boost) => Boost = boost;

    /// <summary>An inbound gate that reaches some way out, drawn by the cars its lanes carry; -1 for none.</summary>
    public int Origin(IReadOnlyList<Gate> gates)
    {
        var total = 0;
        for (var i = 0; i < gates.Count; i++)
            total += gates[i].Inbound && ReachesAny[i] ? gates[i].CarsPerMinute * Boost : 0;
        if (total == 0)
            return -1;
        var pick = random.NextInt(total);
        for (var i = 0; i < gates.Count; i++)
        {
            if (gates[i].Inbound && ReachesAny[i] && (pick -= gates[i].CarsPerMinute * Boost) < 0)
                return i;
        }

        return -1;
    }

    /// <summary>An outbound gate that <paramref name="from"/> reaches, drawn the same way; -1 for none.</summary>
    public int Exit(int from, IReadOnlyList<Gate> gates)
    {
        var n = gates.Count;
        var total = 0;
        for (var to = 0; to < n; to++)
            total += Reach[(from * n) + to] ? gates[to].CarsPerMinute * Boost : 0;
        if (total == 0)
            return -1;
        var pick = random.NextInt(total);
        for (var to = 0; to < n; to++)
        {
            if (Reach[(from * n) + to] && (pick -= gates[to].CarsPerMinute * Boost) < 0)
                return to;
        }

        return -1;
    }
}

/// <summary>A small seeded generator, the same sequence on every machine.</summary>
public sealed class SimRandom(ulong seed)
{
    private ulong _state = seed;

    public int NextInt(int below)
    {
        _state += 0x9E3779B97F4A7C15;
        var z = _state;
        z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9;
        z = (z ^ (z >> 27)) * 0x94D049BB133111EB;
        return (int)((z ^ (z >> 31)) % (ulong)below);
    }
}
