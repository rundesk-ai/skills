using System.Globalization;
using System.Reflection;
using System.Text.Json;

namespace Transit.Sim;

/// <summary>Timed events read from data/events.json: at a tick, the handler named there runs.</summary>
public static class Events
{
    public sealed record Scheduled(long Tick, string Handler);

    public static List<Scheduled> Load(string json) =>
        JsonSerializer.Deserialize<List<Scheduled>>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true }) ?? [];

    /// <summary>Runs the handler named <paramref name="name"/> on <paramref name="sim"/>.</summary>
    public static void Fire(string name, Simulation sim)
    {
        var handler = typeof(Handlers).GetMethod(name, BindingFlags.Public | BindingFlags.Static)
            ?? throw new InvalidOperationException($"no event handler {name}");
        handler.Invoke(null, [sim]);
    }
}

/// <summary>The handlers events name.</summary>
public static class Handlers
{
    public static void OnRushHour(Simulation sim) => sim.Trips.SetBoost(2);

    public static void OnQuietNight(Simulation sim) => sim.Trips.SetBoost(1);
}

/// <summary>Routes in the save file, one per line: id;depot,depot,…;dwell;freight.</summary>
public static class RouteSave
{
    public static string Format(Route route) => string.Join(';',
        route.Id.ToString(CultureInfo.InvariantCulture),
        string.Join(',', route.Depots.Select(d => d.ToString(CultureInfo.InvariantCulture))),
        route.DwellSeconds.ToString("R", CultureInfo.InvariantCulture),
        route.Freight ? "1" : "0");

    public static Route Parse(string line)
    {
        var parts = line.Split(';');
        return new Route(
            int.Parse(parts[0], CultureInfo.InvariantCulture),
            parts[1].Split(',', StringSplitOptions.RemoveEmptyEntries).Select(d => int.Parse(d, CultureInfo.InvariantCulture)).ToArray(),
            float.Parse(parts[2], CultureInfo.InvariantCulture),
            parts[3] == "1");
    }
}
