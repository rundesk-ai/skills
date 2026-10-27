using System.Numerics;
using Transit.Sim;

namespace Transit.Game;

/// <summary>The host engine calls this once a frame, and on the player's tool input.</summary>
public sealed class GameLoop
{
    private readonly Simulation _sim;
    private readonly Planner _planner;
    private readonly List<Events.Scheduled> _events;
    private int _nextEvent;

    public GameLoop(Simulation sim, string eventsJson)
    {
        _sim = sim;
        _planner = new Planner(sim.Network);
        _events = Events.Load(eventsJson);
    }

    public int SelectedVan { get; set; } = -1;

    public int SelectedRoute { get; set; } = -1;

    public void Frame(Canvas canvas, Func<float, Vector2> pointAt)
    {
        _sim.Step();
        while (_nextEvent < _events.Count && _events[_nextEvent].Tick <= _sim.Tick)
            Events.Fire(_events[_nextEvent++].Handler, _sim);

        Hud.Draw(canvas, _sim.Publish());
        if (SelectedVan >= 0)
            Hud.DrawVan(canvas, _sim.Vans, SelectedVan, SelectedRoute);
        if (_sim.KerbCrossing is { } kerb)
            CrossingView.Draw(canvas, kerb.Crossing, Simulation.KerbHalfWidth);
        foreach (var segment in Roads)
            RoadView.Draw(canvas, _sim.Junctions, segment, pointAt, 0f);
    }

    public List<Segment> Roads { get; } = [];

    /// <summary>The track tool: lays a track from an anchor, splitting what it crosses, and stops vans on cut track.</summary>
    public int LayTrack(Anchor from, Vector2 to, IEnumerable<Vector2> crossings, IEnumerable<int> vansOnCutTrack)
    {
        var (track, s) = _planner.Resolve(from);
        _planner.SplitAt(crossings);
        foreach (var van in vansOnCutTrack)
        {
            _sim.Vans.Block(van, true);
            _sim.Vans.Reroute(van);
            _sim.Vans.Block(van, false);
        }

        var start = _sim.Network.HasTrack(track) ? _sim.Network.Track(track).PointAt(s) : from.Point;
        return _sim.Network.Add(start, to);
    }

    /// <summary>The depot tool: places a depot where a platform can stand on track.</summary>
    public int PlaceDepot(Vector2 centre, float along, bool freightOnly) =>
        Siting.CanSite(_sim.Network, centre) ? _sim.Vans.AddDepot(along, freightOnly) : -1;

    /// <summary>The route tool: a new route over existing depots, and its first van.</summary>
    public int AddRoute(int[] depots, float dwellSeconds, bool freight)
    {
        var route = _sim.Vans.AddRoute(depots, dwellSeconds, freight);
        _sim.Vans.Spawn(route, freight ? VanKind.Freight : VanKind.Parcel);
        return route;
    }

    public string SaveRoute(Route route) => RouteSave.Format(route);

    public int LoadRoute(string line)
    {
        var route = RouteSave.Parse(line);
        return AddRoute(route.Depots, route.DwellSeconds, route.Freight);
    }

    public float DepotAt(int depot) => _sim.Vans.Depot(depot).At;

    public int CarArrives(float position, float speed, bool large) =>
        _sim.Kerb.Arrive(position, speed, large ? CarType.Large : CarType.Small);

    public void AddRoad(Segment segment, Control control, float cut)
    {
        Roads.Add(segment);
        _sim.Junctions.Connect(segment);
        _sim.Junctions.SetControl(segment.EndNode, segment.Id, control);
        _sim.Junctions.SetCut(segment.EndNode, segment.Id, cut);
    }

    public void AddGate(int carsPerMinute, bool inbound, bool[] reachesAny, bool[] reach)
    {
        _sim.AddGate(carsPerMinute, inbound);
        _sim.Trips.ReachesAny = reachesAny;
        _sim.Trips.Reach = reach;
    }
}
