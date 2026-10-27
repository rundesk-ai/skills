using System.Numerics;

namespace Harbor.Sim;

/// <summary>A circular arc on the plan: a centre, a radius, and the angles it runs between, radians.</summary>
public sealed record Arc(Vector2 Centre, float Radius, float From, float To)
{
    public float Length => MathF.Abs(To - From) * Radius;

    public Vector2 PointAt(float s)
    {
        var angle = From + (MathF.Sign(To - From) * s / Radius);
        return Centre + (Radius * new Vector2(MathF.Cos(angle), MathF.Sin(angle)));
    }

    /// <summary>The distance along the arc of the point nearest <paramref name="point"/>.</summary>
    public float Closest(Vector2 point)
    {
        var angle = MathF.Atan2(point.Y - Centre.Y, point.X - Centre.X);
        var lo = MathF.Min(From, To);
        var hi = MathF.Max(From, To);
        return MathF.Abs(Math.Clamp(angle, lo, hi) - From) * Radius;
    }
}
