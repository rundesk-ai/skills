using System.Reflection;
using System.Text.Json;

namespace Harbor.Sim;

/// <summary>The whole port, stepped one tick at a time.</summary>
public sealed class Port(ITide tide)
{
    public long Tick { get; private set; }

    public ITide Tide => tide;

    public Fleet Fleet { get; } = new();

    public CraneSystem Cranes { get; } = new();

    public List<Berth> Berths { get; } = [];

    /// <summary>Wind over the quay, metres per second; cranes stop above <see cref="StormWind"/>.</summary>
    public float Wind { get; set; }

    public const float StormWind = 20f;

    public void Step()
    {
        Tick++;
        Fleet.Step(Tick);
        if (Wind < StormWind)
            Cranes.Step(Tick, Fleet);
    }

    public BerthPlan Plan() => Planner.Plan(Berths, Fleet.Ships, tide);

    /// <summary>Test seam: starts the clock at a given tick so a test need not step to it.</summary>
    internal void SetTickForTests(long tick) => Tick = tick;
}

/// <summary>Weather events from data/events.json: at a tick, the handler named there runs.</summary>
public static class Weather
{
    /// <summary>A weather event: when, the handler that applies it, and the icon (a file under assets/icons) the HUD shows.</summary>
    public sealed record Scheduled(long Tick, string Handler, string Icon);

    public static List<Scheduled> Load(string json) =>
        JsonSerializer.Deserialize<List<Scheduled>>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true }) ?? [];

    public static void Fire(string name, Port port) =>
        (typeof(WeatherHandlers).GetMethod(name, BindingFlags.Public | BindingFlags.Static)
            ?? throw new InvalidOperationException($"no weather handler {name}")).Invoke(null, [port]);
}

public static class WeatherHandlers
{
    public static void OnStorm(Port port) => port.Wind = 25f;

    public static void OnCalm(Port port) => port.Wind = 5f;
}
