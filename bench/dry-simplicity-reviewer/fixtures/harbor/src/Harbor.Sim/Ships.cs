namespace Harbor.Sim;

/// <summary>The simulation's clock.</summary>
public static class Clock
{
    public const int TicksPerSecond = 10;

    public static long Ticks(float seconds) => (long)(seconds * TicksPerSecond);
}

public enum ShipState : byte
{
    Approaching,
    Berthed,
    Departing,
    Anchored,
}

/// <summary>A ship: its length and draught in metres, the tick it is due, and the containers stacked fore and aft.</summary>
public sealed class Ship(int id, float length, float draught, long eta)
{
    public int Id => id;

    public float Length => length;

    public float Draught => draught;

    public long Eta => eta;

    public ShipState State { get; set; } = ShipState.Approaching;

    public List<int> Fore { get; } = [];

    public List<int> Aft { get; } = [];
}

/// <summary>The ships in port and what each is doing.</summary>
public sealed class Fleet
{
    private readonly List<Ship> _ships = [];

    /// <summary>Raised when a ship ties up at its berth; the game plays the horn.</summary>
    public event Action<int>? ShipArrived;

    public IReadOnlyList<Ship> Ships => _ships;

    public Ship Add(float length, float draught, long eta)
    {
        var ship = new Ship(_ships.Count, length, draught, eta);
        _ships.Add(ship);
        return ship;
    }

    public void Step(long tick)
    {
        foreach (var ship in _ships)
        {
            switch (ship.State)
            {
                case ShipState.Approaching when tick >= ship.Eta:
                    ship.State = ShipState.Berthed;
                    ShipArrived?.Invoke(ship.Id);
                    break;
                case ShipState.Berthed when ship.Fore.Count == 0 && ship.Aft.Count == 0:
                    ship.State = ShipState.Departing;
                    break;
                case ShipState.Anchored:
                    // An anchored ship waits for the tide before it may approach again.
                    if (tick >= ship.Eta)
                        ship.State = ShipState.Approaching;
                    break;
            }
        }
    }

    /// <summary>Takes the next container off the fore stack; -1 when it is empty.</summary>
    public static int UnloadFore(Ship ship)
    {
        if (ship.Fore.Count == 0)
            return -1;
        var container = ship.Fore[^1];
        ship.Fore.RemoveAt(ship.Fore.Count - 1);
        return container;
    }

    /// <summary>Takes the next container off the aft stack; -1 when it is empty.</summary>
    public static int UnloadAft(Ship ship)
    {
        if (ship.Aft.Count == 0)
            return -1;
        var container = ship.Aft[^1];
        ship.Aft.RemoveAt(ship.Aft.Count - 1);
        return container;
    }
}
