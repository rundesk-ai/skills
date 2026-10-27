using System.Numerics;

namespace Harbor.Game;

/// <summary>What a frame draws: the host engine replays these calls onto the screen.</summary>
public sealed class Canvas
{
    public List<string> Text { get; } = [];

    public List<(string Path, Vector2 At)> Icons { get; } = [];

    public List<(float From, float To, bool Safe)> Bands { get; } = [];

    public void Label(string text) => Text.Add(text);

    public void Icon(string path, Vector2 at) => Icons.Add((path, at));

    public void Band(float from, float to, bool safe) => Bands.Add((from, to, safe));
}
