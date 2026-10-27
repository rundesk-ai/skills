using System.Numerics;

namespace Transit.Sim;

/// <summary>Where a new track is laid from: a track and how far along it, and the point it was picked at.</summary>
public sealed record Anchor(int Track, float S, Vector2 Point);

/// <summary>Lays new track into the network.</summary>
public sealed class Planner(Network network)
{
    /// <summary>Splits every existing track a new one crosses, at the crossing; returns the far pieces.</summary>
    public List<int> SplitAt(IEnumerable<Vector2> crossings)
    {
        var made = new List<int>();
        foreach (var point in crossings)
        {
            if (network.TrackAt(point) is { } crossed)
                made.Add(network.Split(crossed.Track, crossed.S));
        }

        return made;
    }

    /// <summary>The track and distance an anchor lays from; an anchor whose track was split since is found again at its point.</summary>
    public (int Track, float S) Resolve(Anchor anchor) =>
        network.HasTrack(anchor.Track) ? (anchor.Track, anchor.S) : network.TrackAt(anchor.Point) ?? (anchor.Track, anchor.S);
}

/// <summary>Where a depot's platform may stand.</summary>
public static class Siting
{
    /// <summary>Whether a platform centred on <paramref name="centre"/> stands on laid track.</summary>
    public static bool CanSite(Network network, Vector2 centre) => network.TrackAt(centre) is not null;
}
