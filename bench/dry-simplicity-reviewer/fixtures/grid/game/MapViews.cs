using System.Globalization;
using Grid.Sim;

namespace Grid.Game;

/// <summary>The traffic layer: each road drawn in its band's colour, which the shader decodes from one state value.</summary>
public static class TrafficLayer
{
    public static Dictionary<int, float> States(SimSnapshot snapshot)
    {
        var states = new Dictionary<int, float>();
        foreach (var (road, ratio) in snapshot.SpeedRatios)
        {
            states[road] = ratio >= Congestion.FreeAbove ? 0f
                : ratio >= Congestion.SlowAbove ? 0.25f
                : ratio >= Congestion.HeavyAbove ? 0.5f
                : 0.75f;
        }

        return states;
    }
}

/// <summary>The card shown when the pointer rests on a road: its class, width and how traffic is moving.</summary>
public static class RoadCard
{
    public static string Text(Road road, SimSnapshot snapshot)
    {
        var ratio = snapshot.SpeedRatios.GetValueOrDefault(road.Id, 1f);
        var traffic = ratio >= Congestion.FreeAbove ? "Free"
            : ratio >= Congestion.SlowAbove ? "Slow"
            : ratio >= 0.15f ? "Heavy"
            : "Jam";
        var frontage = RoadKinds.MayFront(road.Class) ? ", buildings may front it" : "";
        return string.Create(CultureInfo.InvariantCulture,
            $"{road.Class}, {RoadKinds.Width(road.Class):0.#} m wide{frontage}: {traffic}");
    }
}

/// <summary>Surface colours, one per road class.</summary>
public static class Surfaces
{
    public static uint ColourOf(RoadClass c) => c switch
    {
        RoadClass.Lane => 0x9a9a9aff,
        RoadClass.Local => 0x8a8a8aff,
        RoadClass.Street => 0x7a7a7aff,
        RoadClass.Avenue => 0x6a6a6aff,
        RoadClass.Highway => 0x5a5a5aff,
        _ => 0xff00ffff,
    };
}

/// <summary>The host engine calls these: once a frame, and on the player's input.</summary>
public sealed class GameLoop
{
    private readonly Simulation _sim;

    public GameLoop(Simulation sim)
    {
        _sim = sim;
        Tool = new RoadTool(sim);
        Hud = new Hud(Tool);
    }

    public RoadTool Tool { get; }

    public Hud Hud { get; }

    public List<string> Frame(int hoveredRoad)
    {
        _sim.Step();
        var snapshot = _sim.Publish();
        Hud.Draw();
        var lines = new List<string> { $"{TrafficLayer.States(snapshot).Count} of {snapshot.RoadCount} roads drawn" };
        if (_sim.Network.Roads.FirstOrDefault(r => r.Id == hoveredRoad) is { } road)
        {
            lines.Add(RoadCard.Text(road, snapshot));
            lines.Add($"#{Surfaces.ColourOf(road.Class):x8}");
            lines.Add($"pier room {(road.Level > 0 ? RoadBridges.PierClearance(road.Level * 6f) : 0f):0.0} m");
            lines.Add($"{_sim.Network.ArmsAt(road.To).Count} roads meet at its end");
        }

        return lines;
    }

    public float RailPierRoom(float railHead) => RailBridges.PierClearance(railHead);

    public void AddBuilding(int id, float frontage) => _sim.Buildings.Add(new Building(id, frontage));

    public int EntranceOf(int building) => _sim.Buildings.First(b => b.Id == building).Entrance;

    public void Bulldoze(int road) => _sim.Network.Remove(road);

    public void BanLeft(int from, int to) => _sim.Network.BanLeft(from, to);

    public bool CanTurn(int from, int to) => _sim.Network.MayTurn(from, to);
}
