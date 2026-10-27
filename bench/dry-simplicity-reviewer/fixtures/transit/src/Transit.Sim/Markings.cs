namespace Transit.Sim;

/// <summary>How a junction controls traffic arriving on one road.</summary>
public enum Control : byte
{
    Uncontrolled,
    Yield,
    Stop,
    Signal,
    Priority,
}

/// <summary>A road between two junctions: its lanes each way and its rank (a higher rank takes the way).</summary>
public sealed record Segment(int Id, int StartNode, int EndNode, float Length, int Lanes, int Rank);

/// <summary>The roads meeting at each junction, how each arrival is controlled, and how far back each is cut.</summary>
public sealed class Junctions
{
    private readonly Dictionary<int, List<Segment>> _incident = [];
    private readonly Dictionary<(int Node, int Segment), Control> _control = [];
    private readonly Dictionary<(int Node, int Segment), float> _cut = [];

    public void Connect(Segment segment)
    {
        foreach (var node in (ReadOnlySpan<int>)[segment.StartNode, segment.EndNode])
        {
            if (!_incident.TryGetValue(node, out var list))
                _incident[node] = list = [];
            list.Add(segment);
        }
    }

    public void SetControl(int node, int segment, Control control) => _control[(node, segment)] = control;

    public void SetCut(int node, int segment, float cut) => _cut[(node, segment)] = cut;

    public IReadOnlyList<Segment> Incident(int node) => _incident.TryGetValue(node, out var list) ? list : [];

    public bool IsJunction(int node) => Incident(node).Count > 2;

    public Control ControlOf(int node, int segment) => _control.GetValueOrDefault((node, segment));

    public float CutAt(int node, int segment) => _cut.GetValueOrDefault((node, segment));
}

/// <summary>A painted line along a road, at an offset from its centre, from and to distances along it.</summary>
public readonly record struct MarkingLine(float Offset, float From, float To, bool Dashed);

/// <summary>A bar across the lanes arriving at a junction where they give way; a yield line where they only yield.</summary>
public readonly record struct StopLine(float S, float FromOffset, float ToOffset, bool Yield);

/// <summary>A road's paint: its lines, and its stop or yield lines at each end.</summary>
public sealed record SegmentMarkings(List<MarkingLine> Lines, List<StopLine> StopLines);

/// <summary>Works out a road's paint.</summary>
public static class Markings
{
    public const float LaneWidth = 3.5f;

    public static SegmentMarkings For(Junctions junctions, Segment segment)
    {
        var lines = new List<MarkingLine>();
        var stops = new List<StopLine>();
        var from = Trim(junctions, segment, segment.StartNode);
        var to = segment.Length - Trim(junctions, segment, segment.EndNode);
        if (to - from < 1f)
            return new SegmentMarkings(lines, stops);

        lines.Add(new MarkingLine(0f, from, to, Dashed: false));
        for (var k = 1; k < segment.Lanes; k++)
        {
            lines.Add(new MarkingLine(k * LaneWidth, from, to, Dashed: true));
            lines.Add(new MarkingLine(-k * LaneWidth, from, to, Dashed: true));
        }

        var half = segment.Lanes * LaneWidth;
        if (GivesWay(junctions, segment, segment.EndNode))
        {
            stops.Add(new StopLine(segment.Length - Cut(junctions, segment, segment.EndNode) - 0.5f, 0f, half,
                YieldsOnly(junctions, segment, segment.EndNode)));
        }

        if (GivesWay(junctions, segment, segment.StartNode))
        {
            stops.Add(new StopLine(Cut(junctions, segment, segment.StartNode) + 0.5f, -half, 0f,
                YieldsOnly(junctions, segment, segment.StartNode)));
        }

        return new SegmentMarkings(lines, stops);
    }

    /// <summary>
    /// Whether traffic arriving on <paramref name="segment"/> at <paramref name="node"/> gives way there: its control, or at an
    /// uncontrolled junction another road outranking it.
    /// </summary>
    public static bool GivesWay(Junctions junctions, Segment segment, int node)
    {
        if (!junctions.IsJunction(node))
            return false;
        switch (junctions.ControlOf(node, segment.Id))
        {
            case Control.Stop or Control.Signal or Control.Yield:
                return true;
            case Control.Priority:
                return false;
        }

        foreach (var other in junctions.Incident(node))
        {
            if (other.Id != segment.Id && other.Rank > segment.Rank)
                return true;
        }

        return false;
    }

    /// <summary>How far from <paramref name="node"/> a road's markings stop: past where its junction is cut back, and a metre.</summary>
    public static float Trim(Junctions junctions, Segment segment, int node) => junctions.CutAt(node, segment.Id) + 1f;

    private static float Cut(Junctions junctions, Segment segment, int node) => junctions.CutAt(node, segment.Id);

    private static bool YieldsOnly(Junctions junctions, Segment segment, int node) =>
        junctions.ControlOf(node, segment.Id) is Control.Yield or Control.Uncontrolled;
}
