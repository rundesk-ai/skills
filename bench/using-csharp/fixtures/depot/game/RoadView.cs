using System.Numerics;
using Transit.Sim;

namespace Transit.Game;

/// <summary>Draws a road: its edges, and its lane paint from the sim's markings.</summary>
public static class RoadView
{
    /// <summary>How far paint sits above the road surface, so it never flickers into it.</summary>
    private const float PaintLift = 0.02f;

    public static void Draw(Canvas canvas, Junctions junctions, Segment segment, Func<float, Vector2> pointAt, float height)
    {
        var half = segment.Lanes * Markings.LaneWidth;
        EdgeLine(canvas, segment, pointAt, half, height);
        EdgeLine(canvas, segment, pointAt, -half, height);

        foreach (var line in Markings.For(junctions, segment))
        {
            var a = pointAt(line.From);
            var b = pointAt(line.To);
            canvas.Line(new Vector3(a.X + line.Offset, height + PaintLift, a.Y), new Vector3(b.X + line.Offset, height + PaintLift, b.Y), line.Dashed);
        }
    }

    /// <summary>The road's edge <paramref name="offset"/> to the left of its centre.</summary>
    private static void EdgeLine(Canvas canvas, Segment segment, Func<float, Vector2> pointAt, float offset, float height)
    {
        var a = pointAt(0f);
        var b = pointAt(segment.Length);
        canvas.Line(new Vector3(a.X + offset, height, a.Y), new Vector3(b.X + offset, height, b.Y), dashed: false);
    }
}
