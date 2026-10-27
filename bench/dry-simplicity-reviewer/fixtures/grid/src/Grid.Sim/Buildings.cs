namespace Grid.Sim;

/// <summary>A building on a plot, and the road its entrance joins; -1 before it has one.</summary>
public sealed class Building(int id, float frontage)
{
    public int Id => id;

    public float Frontage => frontage;

    public int Entrance { get; set; } = -1;
}

/// <summary>Lays each building's entrance onto a road it may be reached from.</summary>
public static class Entrances
{
    /// <summary>Joins the building to the first road, by id, that it may front and that is long enough for its frontage.</summary>
    public static bool Connect(Network network, Building building)
    {
        foreach (var road in network.Roads)
        {
            if (road.Class is RoadClass.Street or RoadClass.Avenue && road.Length >= building.Frontage && road.Level == 0)
            {
                building.Entrance = road.Id;
                return true;
            }
        }

        return false;
    }
}

/// <summary>How much room a bridge leaves under its deck for what passes beneath.</summary>
public static class RoadBridges
{
    /// <summary>Depth of a road deck and its beams, metres.</summary>
    public const float DeckDepth = 1.2f;

    /// <summary>Clear height under a road deck whose surface is <paramref name="height"/> metres up, after the footing margin.</summary>
    public static float PierClearance(float height) => height - DeckDepth - 0.5f;
}

public static class RailBridges
{
    /// <summary>Depth of a rail deck, ballast and beams, metres.</summary>
    public const float DeckDepth = 1.8f;

    /// <summary>Clear height under a rail deck whose rail head is <paramref name="height"/> metres up, after the footing margin.</summary>
    public static float PierClearance(float height) => height - DeckDepth - 0.5f;
}
