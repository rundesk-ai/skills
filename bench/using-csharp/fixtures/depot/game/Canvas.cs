using System.Numerics;

namespace Transit.Game;

/// <summary>What a frame draws: the host engine replays these calls onto the screen.</summary>
public sealed class Canvas
{
    public List<string> Text { get; } = [];

    public List<(Vector3 A, Vector3 B, bool Dashed)> Lines { get; } = [];

    public List<(Vector2 Centre, float HalfLength, float HalfWidth)> Openings { get; } = [];

    public void Label(string text) => Text.Add(text);

    public void Line(Vector3 a, Vector3 b, bool dashed) => Lines.Add((a, b, dashed));

    public void Opening(Vector2 centre, float halfLength, float halfWidth) => Openings.Add((centre, halfLength, halfWidth));
}
