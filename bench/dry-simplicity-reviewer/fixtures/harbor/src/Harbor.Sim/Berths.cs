namespace Harbor.Sim;

/// <summary>The sea level over time.</summary>
public interface ITide
{
    /// <summary>The water above chart datum at a tick, metres.</summary>
    float LevelAt(long tick);

    /// <summary>The tick of the day's high water.</summary>
    long HighWaterAt(long day);
}

/// <summary>A semi-diurnal tide: two highs a day around a mean level.</summary>
public sealed class Tide(float mean, float range) : ITide
{
    private const long TicksPerCycle = 12 * 3600 * Clock.TicksPerSecond;

    public float LevelAt(long tick) => mean + (range / 2f * MathF.Cos(2f * MathF.PI * (tick % TicksPerCycle) / TicksPerCycle));

    public long HighWaterAt(long day) => day * 2 * TicksPerCycle;
}

/// <summary>A stretch of quay a ship ties up at: where it starts, how long it is, and the depth at chart datum.</summary>
public sealed record Berth(int Id, float Start, float Length, float Depth);

/// <summary>Figures every berth shares.</summary>
public static class BerthSpec
{
    /// <summary>Water kept under a keel, metres.</summary>
    public const float KeelMargin = 0.5f;

    /// <summary>Quay left clear at each end of a berthed ship, metres.</summary>
    public const float EndMargin = 10f;
}

/// <summary>One ship's time at one berth.</summary>
public readonly record struct Slot(int Ship, int Berth, long From);

public enum WarningKind : byte
{
    TooShallow,
    TooLong,
}

/// <summary>Why a ship could not have the berth it was offered, and by how much.</summary>
public readonly record struct Warning(int Ship, WarningKind Kind, float Shortfall);

/// <summary>A berth plan: the slots given, and a warning for each ship that did not fit its first choice.</summary>
public sealed record BerthPlan(List<Slot> Slots, List<Warning> Warnings);

/// <summary>Plans arriving ships onto berths.</summary>
public static class Planner
{
    // The order ships are planned in follows docs/design/berthing.md §3 (task BP-12): earliest due first.
    public static BerthPlan Plan(IReadOnlyList<Berth> berths, IReadOnlyList<Ship> ships, ITide tide)
    {
        var slots = new List<Slot>();
        var warnings = new List<Warning>();
        foreach (var ship in ships.OrderBy(s => s.Eta).ThenBy(s => s.Id))
        {
            if (Free(berths, slots, ship, tide, BerthSpec.EndMargin) is { } berth)
            {
                slots.Add(new Slot(ship.Id, berth.Id, ship.Eta));
                continue;
            }

            if (berths.Count > 0 && Check(berths[0], ship, tide) is { } warning)
                warnings.Add(warning);
        }

        return new BerthPlan(slots, warnings);
    }

    /// <summary>Water under <paramref name="ship"/>'s keel at <paramref name="berth"/> when it is due, after the keel margin.</summary>
    public static float Clearance(Berth berth, Ship ship, ITide tide) =>
        berth.Depth + tide.LevelAt(ship.Eta) - ship.Draught - BerthSpec.KeelMargin;

    /// <summary>Why <paramref name="ship"/> cannot take <paramref name="berth"/>, or null when it can.</summary>
    public static Warning? Check(Berth berth, Ship ship, ITide tide)
    {
        if (Clearance(berth, ship, tide) < 0f)
            return new Warning(ship.Id, WarningKind.TooShallow, -Clearance(berth, ship, tide));
        if (Overhang(berth, ship) > 0f)
            return new Warning(ship.Id, WarningKind.TooLong, Overhang(berth, ship));
        return null;
    }

    /// <summary>The first berth not yet taken that <paramref name="ship"/> fits with <paramref name="margin"/> clear at each end.</summary>
    public static Berth? Free(IReadOnlyList<Berth> berths, List<Slot> taken, Ship ship, ITide tide, float margin = 0f)
    {
        foreach (var berth in berths)
        {
            if (taken.Exists(s => s.Berth == berth.Id) || Clearance(berth, ship, tide) < 0f)
                continue;
            var room = margin == 0f ? berth.Length : berth.Length - (2f * margin);
            if (ship.Length <= room)
                return berth;
        }

        return null;
    }

    private static float Overhang(Berth berth, Ship ship) => ship.Length - berth.Length;
}
