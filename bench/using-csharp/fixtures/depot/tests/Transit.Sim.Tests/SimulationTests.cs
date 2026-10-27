using System.Numerics;
using Transit.Sim;

namespace Transit.Sim.Tests;

public sealed class SimulationTests
{
    [Fact]
    public void AVanStopsAtEachDepotAndMovesOn()
    {
        var sim = new Simulation(seed: 7, lanes: 1, cars: 8);
        var a = sim.Vans.AddDepot(0f, freightOnly: false);
        var b = sim.Vans.AddDepot(400f, freightOnly: false);
        var route = sim.Vans.AddRoute([a, b], dwellSeconds: 20f, freight: false);
        var van = sim.Vans.Spawn(route, VanKind.Parcel);

        for (var i = 0; i < 20 * Clock.TicksPerSecond; i++)
            sim.Step();

        Assert.True(sim.Vans.Position(van) > 0f);
    }

    [Fact]
    public void AParcelVanPassesAFreightOnlyDepotWithoutStopping()
    {
        var sim = new Simulation(seed: 7, lanes: 1, cars: 8);
        var a = sim.Vans.AddDepot(0f, freightOnly: false);
        var freight = sim.Vans.AddDepot(200f, freightOnly: true);
        var b = sim.Vans.AddDepot(400f, freightOnly: false);
        var route = sim.Vans.AddRoute([a, freight, b], dwellSeconds: 20f, freight: false);
        var van = sim.Vans.Spawn(route, VanKind.Parcel);

        for (var i = 0; i < 45 * Clock.TicksPerSecond; i++)
            sim.Step();

        Assert.True(sim.Vans.Position(van) > 200f);
    }

    [Fact]
    public void TripsAreCountedAsTheyStart()
    {
        var sim = new Simulation(seed: 7, lanes: 1, cars: 8);
        sim.AddGate(10, inbound: true);
        sim.AddGate(10, inbound: false);
        sim.Trips.ReachesAny = [true, false];
        sim.Trips.Reach = [false, true, false, false];

        sim.Step();

        Assert.Equal(1, sim.Publish().TripsStarted);
    }

    [Fact]
    public void ANewVanJoinsARouteEveryTwoMinutes()
    {
        var sim = new Simulation(seed: 7, lanes: 1, cars: 8);
        var a = sim.Vans.AddDepot(0f, freightOnly: false);
        var b = sim.Vans.AddDepot(400f, freightOnly: false);
        sim.Vans.AddRoute([a, b], dwellSeconds: 20f, freight: false);
        sim.Vans.AddRoute([b, a], dwellSeconds: 20f, freight: false);
        sim.SetTickForTests(Clock.Ticks(120f) - 1);

        sim.Step();

        Assert.Equal(1, sim.Vans.Count);
    }

    [Fact]
    public void ParcelsHandedInWaitUntilAVanCalls()
    {
        var sim = new Simulation(seed: 7, lanes: 1, cars: 8);
        var a = sim.Vans.AddDepot(0f, freightOnly: false);
        var b = sim.Vans.AddDepot(400f, freightOnly: false);
        var route = sim.Vans.AddRoute([a, b], dwellSeconds: 20f, freight: false);
        sim.Vans.HandIn(b, 5);
        Assert.Equal(5, sim.Vans.WaitingOn(route));

        sim.Vans.Spawn(route, VanKind.Parcel);
        for (var i = 0; i < 40 * Clock.TicksPerSecond; i++)
            sim.Step();

        Assert.Equal(0, sim.Vans.WaitingOn(route));
    }

    [Fact]
    public void ACarWaitsBehindTheCrossing()
    {
        var sim = new Simulation(seed: 7, lanes: 1, cars: 8);
        sim.KerbCrossing = (new Crossing(Vector2.Zero, Vector2.UnitX, Vector2.UnitY, Reach: 4f), 100f);
        sim.Bays.Add(110f);
        sim.Kerb.Arrive(80f, 10f, CarType.Small);

        sim.Step();

        Assert.Equal(0, sim.Parking.ParkedCount);
    }
}
