using Transit.Sim;

namespace Transit.Sim.Tests;

public sealed class MarkingsTests
{
    [Fact]
    public void ATwoLaneRoadHasACentreLineAndALaneLineEachSide()
    {
        var junctions = new Junctions();
        var road = new Segment(0, 0, 1, 100f, 2);

        var lines = Markings.For(junctions, road);

        Assert.Equal(3, lines.Count);
        Assert.Single(lines, l => !l.Dashed);
    }

    [Fact]
    public void PaintStopsShortOfAJunctionsCut()
    {
        var junctions = new Junctions();
        var road = new Segment(0, 0, 1, 100f, 1);
        junctions.SetCut(1, 0, 12f);

        var line = Assert.Single(Markings.For(junctions, road));

        Assert.Equal(87f, line.To);
    }
}
