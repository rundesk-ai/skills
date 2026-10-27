namespace Grid.Sim;

public enum RoadClass : byte
{
    Lane,
    Local,
    Street,
    Avenue,
    Highway,
}

public static class RoadKinds
{
    /// <summary>Whether a class is a town street that buildings may front and be reached from.</summary>
    public static bool MayFront(RoadClass c) => c is RoadClass.Local or RoadClass.Street or RoadClass.Avenue;

    /// <summary>Carriageway width, metres.</summary>
    public static float Width(RoadClass c) => c switch
    {
        RoadClass.Lane => 3.5f,
        RoadClass.Local => 6.6f,
        RoadClass.Street => 11f,
        RoadClass.Avenue => 18f,
        RoadClass.Highway => 24f,
        _ => throw new ArgumentOutOfRangeException(nameof(c)),
    };
}

/// <summary>The levels a road may be built at: tunnels below zero, bridges above.</summary>
public static class Levels
{
    public const int Lowest = -2;
    public const int Highest = 3;
}

public sealed record Road(int Id, RoadClass Class, float Length, int Level, int From, int To);

/// <summary>The roads and the junctions they meet at, and the left turns banned at each junction.</summary>
public sealed class Network
{
    private readonly Dictionary<int, Road> _roads = [];
    private readonly Dictionary<int, List<int>> _arms = [];
    private readonly HashSet<(int From, int To)> _noLeft = [];
    private int _next;

    public IEnumerable<Road> Roads => _roads.Values.OrderBy(r => r.Id);

    public Road Add(RoadClass roadClass, float length, int level, int from, int to)
    {
        var road = new Road(_next++, roadClass, length, level, from, to);
        _roads[road.Id] = road;
        foreach (var node in (ReadOnlySpan<int>)[from, to])
        {
            if (!_arms.TryGetValue(node, out var arms))
                _arms[node] = arms = [];
            arms.Add(road.Id);
        }

        return road;
    }

    public void Remove(int id)
    {
        if (!_roads.Remove(id, out var road))
            return;
        _arms[road.From].Remove(id);
        _arms[road.To].Remove(id);
    }

    public void BanLeft(int from, int to) => _noLeft.Add((from, to));

    /// <summary>Whether a car may turn from one road onto another at their shared junction.</summary>
    public bool MayTurn(int from, int to) => _roads.ContainsKey(from) && _roads.ContainsKey(to) && !_noLeft.Contains((from, to));

    public IReadOnlyList<int> ArmsAt(int node) => _arms.TryGetValue(node, out var arms) ? arms : [];
}
