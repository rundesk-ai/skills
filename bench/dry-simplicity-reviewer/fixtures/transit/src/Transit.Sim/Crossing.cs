using System.Numerics;

namespace Transit.Sim;

/// <summary>A level crossing: where a road crosses track, the two directions, and how far its deck reaches each way.</summary>
public sealed record Crossing(Vector2 Point, Vector2 TrackDirection, Vector2 RoadDirection, float Reach)
{
    /// <summary>The shallowest crossing the deck is worked out for; a shallower one is treated as this skew.</summary>
    public const float MinSine = 0.2f;

    /// <summary>
    /// How far along the road a square opening across a band <paramref name="halfWidth"/> either side of the road's
    /// centre must reach to clear the whole skewed deck, plus <paramref name="margin"/>.
    /// </summary>
    public float SquareReach(float halfWidth, float margin)
    {
        var cross = (TrackDirection.X * RoadDirection.Y) - (TrackDirection.Y * RoadDirection.X);
        var sine = MathF.Max(MinSine, MathF.Abs(cross));
        return Reach + (halfWidth * MathF.Abs(Vector2.Dot(TrackDirection, RoadDirection)) / sine) + margin;
    }

    /// <summary>How far back from the crossing a car on a road <paramref name="halfWidth"/> wide each side stops.</summary>
    public float StopBack(float halfWidth) => SquareReach(halfWidth, 2f);
}
