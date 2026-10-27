namespace Transit.Sim;

public enum VanKind : byte
{
    Parcel,
    Freight,
}

/// <summary>A depot vans call at; a freight-only depot is passed by parcel vans.</summary>
public sealed record Depot(int Id, float At, bool FreightOnly);

/// <summary>A van route: the depots in order, looping back to the first, and how long its parcel vans stand at each.</summary>
public sealed record Route(int Id, int[] Depots, float DwellSeconds, bool Freight);

/// <summary>Every van: where it is on its route, how fast it goes, and how long it stands; and the parcels waiting at each depot.</summary>
public sealed class VanSystem
{
    private const float CurveStep = 5f;

    /// <summary>How near a depot it passes a van first plans its next leg: its braking distance from top speed, and a margin.</summary>
    private const float PassReach = VanSpec.BrakingDistance + 50f;

    private readonly List<Route> _routes = [];
    private readonly List<Depot> _depots = [];
    private readonly List<int> _waiting = [];
    private readonly List<float> _speed = [];
    private readonly List<float> _position = [];
    private readonly List<float> _dwell = [];
    private readonly List<int> _route = [];
    private readonly List<int> _stop = [];
    private readonly List<VanKind> _kind = [];
    private readonly List<bool> _alive = [];
    private readonly List<bool> _blocked = [];

    public int Count { get; private set; }

    public int RouteCount => _routes.Count;

    public int AddRoute(int[] depots, float dwellSeconds, bool freight)
    {
        _routes.Add(new Route(_routes.Count, depots, dwellSeconds, freight));
        return _routes.Count - 1;
    }

    public int AddDepot(float at, bool freightOnly)
    {
        _depots.Add(new Depot(_depots.Count, at, freightOnly));
        _waiting.Add(0);
        return _depots.Count - 1;
    }

    public Depot Depot(int id) => _depots[id];

    /// <summary>Parcels handed in at a depot, waiting for a van.</summary>
    public void HandIn(int depot, int parcels) => _waiting[depot] += parcels;

    /// <summary>The parcels waiting at every depot route <paramref name="route"/> calls at.</summary>
    public int WaitingOn(int route)
    {
        var total = 0;
        foreach (var depot in _routes[route].Depots.Distinct())
            total += _waiting[depot];
        return total;
    }

    public int Spawn(int route, VanKind kind)
    {
        _speed.Add(0f);
        _position.Add(_depots[_routes[route].Depots[0]].At);
        _dwell.Add(0f);
        _route.Add(route);
        _stop.Add(1);
        _kind.Add(kind);
        _alive.Add(true);
        _blocked.Add(false);
        Count++;

        // A route with one depot has nowhere to go yet: the van waits and tries again.
        if (_routes[route].Depots.Length < 2)
            _dwell[^1] = VanSpec.RetrySeconds;
        return _speed.Count - 1;
    }

    public float Speed(int van) => _speed[van];

    public float Position(int van) => _position[van];

    public void Block(int van, bool blocked) => _blocked[van] = blocked;

    public void Step(float dt)
    {
        for (var v = 0; v < _speed.Count; v++)
        {
            if (!_alive[v])
                continue;
            if (_dwell[v] > 0f)
            {
                _dwell[v] -= dt;
                continue;
            }

            if (_blocked[v])
            {
                _speed[v] = 0f;
                _dwell[v] = VanSpec.RetrySeconds;
                continue;
            }

            _speed[v] = MathF.Min(_speed[v] + (VanSpec.Braking * dt), Limit(v));
            _position[v] += _speed[v] * dt;
            var route = _routes[_route[v]];
            var depot = route.Depots[_stop[v] % route.Depots.Length];
            if (_position[v] >= _depots[depot].At)
            {
                _position[v] = _depots[depot].At;
                _speed[v] = 0f;
                _dwell[v] = DwellFor(route, _stop[v], _kind[v]);
                if (_dwell[v] > 0f)
                    _waiting[depot] = 0;
                _stop[v]++;
                if (_stop[v] > route.Depots.Length * 4)
                    Retire(v);
            }
        }
    }

    /// <summary>The speed a van may run at: it must be able to stop at its next depot, so it slows within braking reach of it.</summary>
    public float Limit(int v)
    {
        var route = _routes[_route[v]];
        var next = _depots[route.Depots[_stop[v] % route.Depots.Length]].At;
        var toGo = next - _position[v];
        if (toGo > VanSpec.BrakingDistance + CurveStep || DwellFor(route, _stop[v], _kind[v]) == 0f && toGo > PassReach)
            return VanSpec.MaxSpeed;
        return MathF.Max(1f, MathF.Sqrt(2f * VanSpec.Braking * MathF.Max(0f, toGo)));
    }

    /// <summary>Sends a van back to the first depot of its route, as when its line ahead is cut.</summary>
    public void Reroute(int v)
    {
        var route = _routes[_route[v]];
        if (route.Depots.Length == 0)
        {
            _dwell[v] = VanSpec.RetrySeconds;
            return;
        }

        _stop[v] = 0;
        _position[v] = _depots[route.Depots[0]].At;
    }

    /// <summary>
    /// How long a <paramref name="kind"/> van stands at stop <paramref name="stop"/> of <paramref name="route"/>: none at a
    /// freight-only depot a parcel van passes.
    /// </summary>
    private float DwellFor(Route route, int stop, VanKind kind)
    {
        var depot = _depots[route.Depots[stop % route.Depots.Length]];
        if (depot.FreightOnly && kind != VanKind.Freight)
            return 0f;
        return kind == VanKind.Freight ? VanSpec.FreightDwell : route.DwellSeconds;
    }

    /// <summary>Seconds a van takes round its route at top speed, standing where its vans stand.</summary>
    public float RoundTripSeconds(int routeId)
    {
        var route = _routes[routeId];
        var kind = route.Freight ? VanKind.Freight : VanKind.Parcel;
        var seconds = 0f;
        for (var stop = 0; stop < route.Depots.Length; stop++)
        {
            var from = _depots[route.Depots[stop]].At;
            var to = _depots[route.Depots[(stop + 1) % route.Depots.Length]].At;
            seconds += (MathF.Abs(to - from) / VanSpec.MaxSpeed) + DwellFor(route, stop + 1, kind);
        }

        return seconds;
    }

    /// <summary>Takes a van off the map.</summary>
    public void Retire(int v)
    {
        _alive[v] = false;
        Count--;
    }
}
