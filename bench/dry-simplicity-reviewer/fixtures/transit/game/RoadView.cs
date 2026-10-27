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
        EdgeLine(canvas, segment, pointAt, half, height, 0f);
        EdgeLine(canvas, segment, pointAt, -half, height, 0f);

        var markings = Markings.For(junctions, segment);
        foreach (var line in markings.Lines)
        {
            var a = pointAt(line.From);
            var b = pointAt(line.To);
            canvas.Line(new Vector3(a.X + line.Offset, height + PaintLift, a.Y), new Vector3(b.X + line.Offset, height + PaintLift, b.Y), line.Dashed);
        }
    }

    /// <summary>The road's edge <paramref name="offset"/> to the left of its centre, raised <paramref name="lift"/> above it.</summary>
    private static void EdgeLine(Canvas canvas, Segment segment, Func<float, Vector2> pointAt, float offset, float height, float lift)
    {
        var a = pointAt(0f);
        var b = pointAt(segment.Length);
        canvas.Line(new Vector3(a.X + offset, height + lift, a.Y), new Vector3(b.X + offset, height + lift, b.Y), dashed: false);
    }
}
