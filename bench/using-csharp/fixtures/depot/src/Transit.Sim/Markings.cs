namespace Transit.Sim;

/// <summary>A road between two junctions, and its lanes each way.</summary>
public sealed record Segment(int Id, int StartNode, int EndNode, float Length, int Lanes);

/// <summary>How far back each junction is cut along each road that meets it.</summary>
public sealed class Junctions
{
    private readonly Dictionary<(int Node, int Segment), float> _cut = [];

    public void SetCut(int node, int segment, float cut) => _cut[(node, segment)] = cut;

    public float CutAt(int node, int segment) => _cut.GetValueOrDefault((node, segment));
}

/// <summary>A painted line along a road, at an offset from its centre, from and to distances along it.</summary>
public readonly record struct MarkingLine(float Offset, float From, float To, bool Dashed);

/// <summary>Works out a road's paint.</summary>
public static class Markings
{
    public const float LaneWidth = 3.5f;

    /// <summary>A road's lines: a solid centre line, and a dashed line between its lanes each way.</summary>
    public static List<MarkingLine> For(Junctions junctions, Segment segment)
    {
        var lines = new List<MarkingLine>();
        var from = Trim(junctions, segment, segment.StartNode);
        var to = segment.Length - Trim(junctions, segment, segment.EndNode);
        if (to - from < 1f)
            return lines;

        lines.Add(new MarkingLine(0f, from, to, Dashed: false));
        for (var k = 1; k < segment.Lanes; k++)
        {
            lines.Add(new MarkingLine(k * LaneWidth, from, to, Dashed: true));
            lines.Add(new MarkingLine(-k * LaneWidth, from, to, Dashed: true));
        }

        return lines;
    }

    /// <summary>How far from <paramref name="node"/> a road's markings stop: past where its junction is cut back, and a metre.</summary>
    public static float Trim(Junctions junctions, Segment segment, int node) => junctions.CutAt(node, segment.Id) + 1f;
}
