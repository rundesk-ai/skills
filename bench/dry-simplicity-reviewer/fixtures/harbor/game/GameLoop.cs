using System.Globalization;
using System.Numerics;
using Harbor.Sim;

namespace Harbor.Game;

/// <summary>The host engine calls these: once a frame, and on the player's tool input.</summary>
public sealed class GameLoop
{
    private readonly Port _port;
    private readonly List<Weather.Scheduled> _weather;
    private int _next;
    private string? _weatherIcon;

    public GameLoop(Port port, string eventsJson)
    {
        _port = port;
        _weather = Weather.Load(eventsJson);
        _port.Fleet.ShipArrived += ship => Horns.Add(ship);
    }

    /// <summary>Ships whose horn the host plays this frame.</summary>
    public List<int> Horns { get; } = [];

    public Ship? Selected { get; set; }

    public void Frame(Canvas canvas)
    {
        Horns.Clear();
        _port.Step();
        while (_next < _weather.Count && _weather[_next].Tick <= _port.Tick)
        {
            Weather.Fire(_weather[_next].Handler, _port);
            _weatherIcon = _weather[_next++].Icon;
        }

        if (_weatherIcon is not null)
            canvas.Icon($"assets/icons/{_weatherIcon}.svg", Vector2.Zero);
        QuayView.Draw(canvas, _port, Selected);
        for (var c = 0; c < _port.Cranes.Count; c++)
        {
            var until = _port.Cranes.BusyUntil(c);
            canvas.Label(string.Create(CultureInfo.CurrentCulture, $"Crane {c}: {(until > _port.Tick ? "busy" : "free")}"));
        }

        if (Selected is { } ship)
        {
            var remaining = ship.Fore.Count + ship.Aft.Count;
            var finish = _port.Cranes.Count > 0 ? _port.Cranes.EstimateFinish(0, remaining, ship.Length, _port.Tick) : -1;
            canvas.Label(string.Create(CultureInfo.CurrentCulture, $"Ship {ship.Id}: done at tick {finish}"));
        }
    }

    public Ship AddShip(float length, float draught, long eta, int containers)
    {
        var ship = _port.Fleet.Add(length, draught, eta);
        for (var i = 0; i < containers; i++)
            (i % 2 == 0 ? ship.Fore : ship.Aft).Add(i);
        return ship;
    }

    public void AddBerth(float start, float length, float depth) =>
        _port.Berths.Add(new Berth(_port.Berths.Count, start, length, depth));

    public void AddCrane(float boomAt, int ship) => _port.Cranes.Assign(_port.Cranes.Add(boomAt), ship);
}
