namespace Transit.Sim;

/// <summary>
/// Steps the cars on the kerbside lane: each looks for a bay ahead, claims it when no car behind would run into it,
/// brakes for it and parks; a parked car pulls out at the head of the lane when the car behind can stop.
/// </summary>
public sealed class KerbDriver(Parking parking, LaneQueue queue)
{
    private const int Lane = 0;

    // Parked cars waiting to pull out, by car, and the tick each began to wait; sorted so the order is the same every run.
    private readonly SortedDictionary<int, long> _waiting = [];

    public void Step(long tick, IReadOnlyList<float> bays, float crossingHold)
    {
        for (var car = 0; car < parking.Count; car++)
        {
            if (_waiting.ContainsKey(car))
                continue;
            var bay = NextBay(bays, parking.Position(car));
            if (bay < 0 || bays[bay] > crossingHold)
                continue;
            if (parking.GivesUpClaim(car, tick))
                continue;
            if (!parking.CanClaim(car, bays[bay]))
                continue;
            parking.Claim(car, bay, tick);
            if (parking.Position(car) >= parking.BrakeFrom(car, bays[bay]))
            {
                queue.Leave(car, Lane);
                parking.Park(car);
                _waiting[car] = tick;
            }
        }

        foreach (var (car, since) in _waiting.ToList())
        {
            if (parking.CanPullOut(queue.Head(Lane), parking.Position(car)))
            {
                queue.JoinAtHead(car, Lane);
                _waiting.Remove(car);
            }
            else if (parking.GivesUpPullOut(car, since, tick))
            {
                _waiting.Remove(car);
            }
        }
    }

    /// <summary>Adds a car arriving on the lane at its tail.</summary>
    public int Arrive(float position, float speed, CarType type)
    {
        var car = parking.Add(position, speed, type);
        queue.Join(car, Lane);
        return car;
    }

    private static int NextBay(IReadOnlyList<float> bays, float position)
    {
        for (var i = 0; i < bays.Count; i++)
        {
            if (bays[i] >= position)
                return i;
        }

        return -1;
    }
}
