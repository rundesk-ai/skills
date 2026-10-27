using System.Numerics;
using Transit.Sim;

namespace Transit.Game;

/// <summary>Draws a level crossing: the gap in the road's paint where the deck lies.</summary>
public static class CrossingView
{
    /// <summary>Clear of the deck's edge by this much, metres.</summary>
    private const float PaintMargin = 0.5f;

    public static void Draw(Canvas canvas, Crossing crossing, float roadHalfWidth)
    {
        var reach = Reach(crossing, roadHalfWidth, PaintMargin);
        canvas.Opening(crossing.Point, reach, roadHalfWidth);
    }

    /// <summary>A square opening across a band, outside the whole skew deck at that band's width.</summary>
    private static float Reach(Crossing crossing, float halfWidth, float margin)
    {
        var sine = MathF.Max(0.25f, MathF.Abs((crossing.TrackDirection.X * crossing.RoadDirection.Y)
            - (crossing.TrackDirection.Y * crossing.RoadDirection.X)));
        return crossing.Reach + (halfWidth * MathF.Abs(Vector2.Dot(crossing.TrackDirection, crossing.RoadDirection)) / sine) + margin;
    }
}
