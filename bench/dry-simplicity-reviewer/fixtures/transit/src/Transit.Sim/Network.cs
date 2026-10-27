using System.Numerics;

namespace Transit.Sim;

/// <summary>A straight run of track from one point to another.</summary>
public sealed record Track(int Id, Vector2 Start, Vector2 End)
{
    public float Length => Vector2.Distance(Start, End);

    /// <summary>How far along the track its point nearest <paramref name="point"/> lies, and how far away that is.</summary>
    public (float S, float Distance) Closest(Vector2 point)
    {
        var direction = End - Start;
        var t = Math.Clamp(Vector2.Dot(point - Start, direction) / direction.LengthSquared(), 0f, 1f);
        return (t * Length, Vector2.Distance(Start + (direction * t), point));
    }

    public Vector2 PointAt(float s) => Vector2.Lerp(Start, End, s / Length);
}

/// <summary>The laid track.</summary>
public sealed class Network
{
    private readonly List<Track?> _tracks = [];

    public int Add(Vector2 start, Vector2 end)
    {
        _tracks.Add(new Track(_tracks.Count, start, end));
        return _tracks.Count - 1;
    }

    public Track Track(int id) => _tracks[id] ?? throw new ArgumentException($"no track {id}", nameof(id));

    public bool HasTrack(int id) => id >= 0 && id < _tracks.Count && _tracks[id] is not null;

    /// <summary>Adds to <paramref name="into"/> every track whose bounds come within <paramref name="radius"/> of a point.</summary>
    public void QueryNear(Vector2 point, float radius, List<int> into)
    {
        foreach (var track in _tracks)
        {
            if (track is null)
                continue;
            var min = Vector2.Min(track.Start, track.End) - new Vector2(radius);
            var max = Vector2.Max(track.Start, track.End) + new Vector2(radius);
            if (point.X >= min.X && point.Y >= min.Y && point.X <= max.X && point.Y <= max.Y)
                into.Add(track.Id);
        }
    }

    /// <summary>Splits track <paramref name="id"/> at <paramref name="s"/> metres; returns the id of the far piece.</summary>
    public int Split(int id, float s)
    {
        var track = Track(id);
        var at = track.PointAt(s);
        _tracks[id] = track with { End = at };
        return Add(at, track.End);
    }
}
