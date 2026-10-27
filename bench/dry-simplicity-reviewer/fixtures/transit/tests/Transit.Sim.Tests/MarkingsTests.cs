using Transit.Sim;

namespace Transit.Sim.Tests;

public sealed class MarkingsTests
{
    [Fact]
    public void AStreetGivesWayToAMainRoadAtAnUncontrolledJunction()
    {
        var junctions = new Junctions();
        var street = new Segment(0, 0, 1, 100f, 1, Rank: 1);
        var main = new Segment(1, 1, 2, 100f, 2, Rank: 3);
        var other = new Segment(2, 1, 3, 100f, 2, Rank: 3);
        junctions.Connect(street);
        junctions.Connect(main);
        junctions.Connect(other);

        Assert.True(Markings.GivesWay(junctions, street, 1));
        Assert.False(Markings.GivesWay(junctions, main, 1));
    }

    [Fact]
    public void ATwoLaneRoadHasACentreLineAndALaneLineEachSide()
    {
        var junctions = new Junctions();
        var road = new Segment(0, 0, 1, 100f, 2, Rank: 2);
        junctions.Connect(road);

        var markings = Markings.For(junctions, road);

        Assert.Equal(3, markings.Lines.Count);
        Assert.Single(markings.Lines, l => !l.Dashed);
    }
}
