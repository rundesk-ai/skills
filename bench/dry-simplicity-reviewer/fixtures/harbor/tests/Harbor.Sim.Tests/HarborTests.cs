using System.Numerics;
using Harbor.Sim;

namespace Harbor.Sim.Tests;

/// <summary>A tide that never moves, so a test reads depths directly.</summary>
internal sealed class FlatTide(float level) : ITide
{
    public float LevelAt(long tick) => level;

    public long HighWaterAt(long day) => 0;
}

public sealed class HarborTests
{
    [Fact]
    public void AShipIsPlannedOntoTheFirstBerthItFloatsAndFitsAt()
    {
        var port = new Port(new FlatTide(1f));
        port.Berths.Add(new Berth(0, 0f, 150f, 8f));
        port.Berths.Add(new Berth(1, 200f, 300f, 14f));
        port.Fleet.Add(length: 220f, draught: 12f, eta: 100);

        var plan = port.Plan();

        Assert.Equal(1, Assert.Single(plan.Slots).Berth);
    }

    [Fact]
    public void AShipThatFitsNowhereIsWarnedAboutTheFirstBerth()
    {
        var tide = new FlatTide(0f);
        var berth = new Berth(0, 0f, 150f, 8f);
        var ship = new Ship(0, 120f, 9f, 0);

        var warning = Planner.Check(berth, ship, tide);

        Assert.Equal(WarningKind.TooShallow, warning?.Kind);
    }

    [Fact]
    public void ACraneEmptiesItsStackThenFreesTheShip()
    {
        var port = new Port(new FlatTide(1f));
        var ship = port.Fleet.Add(100f, 8f, eta: 0);
        ship.Fore.AddRange([1, 2]);
        port.Cranes.Assign(port.Cranes.Add(0f), ship.Id);

        for (var i = 0; i < 200; i++)
            port.Step();

        Assert.Empty(ship.Fore);
        Assert.Equal(ShipState.Departing, ship.State);
    }

    [Fact]
    public void CranesStopInAStorm()
    {
        var port = new Port(new FlatTide(1f));
        var ship = port.Fleet.Add(100f, 8f, eta: 0);
        ship.Fore.AddRange([1, 2]);
        port.Cranes.Assign(port.Cranes.Add(0f), ship.Id);
        WeatherHandlers.OnStorm(port);

        for (var i = 0; i < 200; i++)
            port.Step();

        Assert.Equal(2, ship.Fore.Count);
    }

    [Fact]
    public void AnArcsPointsLieOnItsCircle()
    {
        var arc = new Arc(Vector2.Zero, 10f, 0f, MathF.PI / 2f);

        Assert.Equal(10f, arc.PointAt(arc.Length / 2f).Length(), 3);
        Assert.Equal(arc.Length, arc.Closest(new Vector2(0f, 20f)), 3);
    }

    [Fact]
    public void TheClockStartsWhereATestPutsIt()
    {
        var port = new Port(new FlatTide(1f));
        port.SetTickForTests(500);

        port.Step();

        Assert.Equal(501, port.Tick);
    }
}
