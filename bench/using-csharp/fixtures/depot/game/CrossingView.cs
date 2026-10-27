using Transit.Sim;

namespace Transit.Game;

/// <summary>Draws a level crossing: the gap in the road's paint where the deck lies.</summary>
public static class CrossingView
{
    /// <summary>Clear of the deck's edge by this much, metres.</summary>
    private const float PaintMargin = 0.5f;

    public static void Draw(Canvas canvas, Crossing crossing, float roadHalfWidth) =>
        canvas.Opening(crossing.Point, crossing.SquareReach(roadHalfWidth, PaintMargin), roadHalfWidth);
}
