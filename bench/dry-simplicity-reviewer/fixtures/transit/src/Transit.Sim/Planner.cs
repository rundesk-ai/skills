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
            var (crossed, at) = TrackAt(point);
            if (crossed >= 0)
                made.Add(network.Split(crossed, at));
        }

        return made;
    }

    /// <summary>The track and distance an anchor lays from; an anchor whose track was split since is found again at its point.</summary>
    public (int Track, float S) Resolve(Anchor anchor)
    {
        var (id, s) = (anchor.Track, anchor.S);
        if (!network.HasTrack(id))
        {
            var near = new List<int>();
            network.QueryNear(anchor.Point, 1f, near);
            foreach (var candidate in near)
            {
                var (at, distance) = network.Track(candidate).Closest(anchor.Point);
                if (distance < 0.5f)
                {
                    (id, s) = (candidate, at);
                    break;
                }
            }
        }

        return (id, s);
    }

    private (int Track, float S) TrackAt(Vector2 point)
    {
        var near = new List<int>();
        network.QueryNear(point, 1f, near);
        foreach (var candidate in near)
        {
            var (at, distance) = network.Track(candidate).Closest(point);
            if (distance < 0.5f)
                return (candidate, at);
        }

        return (-1, 0f);
    }
}

/// <summary>Where a depot's platform may stand.</summary>
public static class Siting
{
    /// <summary>Whether a platform centred on <paramref name="centre"/> stands on laid track.</summary>
    public static bool CanSite(Network network, Vector2 centre) => TrackUnder(network, centre) is not null;

    /// <summary>The track whose line runs nearest <paramref name="point"/>, within a metre, and how far along it.</summary>
    internal static (int Track, float S)? TrackUnder(Network network, Vector2 point)
    {
        var near = new List<int>();
        network.QueryNear(point, 1f, near);
        foreach (var id in near)
        {
            var (s, distance) = network.Track(id).Closest(point);
            if (distance < 1f)
                return (id, s);
        }

        return null;
    }
}
