namespace Transit.Sim;

/// <summary>What the game reads from the simulation once a tick.</summary>
public sealed record SimSnapshot(long Tick, int VanCount, int ParkedCars, int QueuedCars, float TripsPerMinute);

/// <summary>The whole simulation, stepped one tick at a time.</summary>
public sealed class Simulation
{
    /// <summary>Half the kerb lane's road width, metres.</summary>
    public const float KerbHalfWidth = 3.5f;

    private readonly List<Gate> _gates = [];
    private int _tripsThisMinute;
    private float _tripsPerMinute;

    public Simulation(ulong seed, int lanes, int cars)
    {
        Random = new SimRandom(seed);
        Trips = new TripPicker(Random);
        Queue = new LaneQueue(lanes, cars);
        Kerb = new KerbDriver(Parking, Queue);
    }

    /// <summary>The kerbside bays, metres along the kerb lane.</summary>
    public List<float> Bays { get; } = [];

    /// <summary>The level crossing on the kerb lane, if any, and how far along the lane it lies.</summary>
    public (Crossing Crossing, float S)? KerbCrossing { get; set; }

    public KerbDriver Kerb { get; }

    public long Tick { get; private set; }

    public SimRandom Random { get; }

    public VanSystem Vans { get; } = new();

    public Parking Parking { get; } = new();

    public LaneQueue Queue { get; }

    public TripPicker Trips { get; }

    public Network Network { get; } = new();

    public Junctions Junctions { get; } = new();

    public void AddGate(int carsPerMinute, bool inbound) => _gates.Add(new Gate(carsPerMinute, inbound));

    public void Step()
    {
        Tick++;
        Vans.Step(1f / Clock.TicksPerSecond);
        var hold = KerbCrossing is { } c ? c.S - c.Crossing.StopBack(KerbHalfWidth) : float.MaxValue;
        Kerb.Step(Tick, Bays, hold);
        if (Trips.Origin(_gates) is var origin and >= 0 && Trips.Exit(origin, _gates) >= 0)
            _tripsThisMinute++;
        if (Tick % (60 * Clock.TicksPerSecond) == 0)
        {
            _tripsPerMinute = _tripsThisMinute;
            _tripsThisMinute = 0;
        }
    }

    public SimSnapshot Publish() => new(Tick, Vans.Count, Parking.ParkedCount, QueuedCount(), _tripsPerMinute);

    /// <summary>Test seam: starts the clock mid-day so a test need not step thousands of ticks to reach it.</summary>
    internal void SetTickForTests(long tick) => Tick = tick;

    private int QueuedCount()
    {
        var queued = 0;
        for (var lane = 0; lane < Queue.Lanes; lane++)
        {
            for (var car = Queue.Head(lane); car != LaneQueue.None; car = Queue.Behind(car))
                queued++;
        }

        return queued;
    }
}
