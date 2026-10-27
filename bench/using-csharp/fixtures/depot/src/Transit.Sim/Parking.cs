namespace Transit.Sim;

public enum CarType : byte
{
    Small,
    Large,
}

/// <summary>Cars on one kerbside lane, each either driving or claiming a bay to park in.</summary>
public sealed class Parking
{
    private const float MinGap = 2f;
    private const float ClaimGiveUpSeconds = 30f;
    private const float PullOutGiveUpSeconds = 45f;

    private readonly float[] _braking = [4.5f, 3f];
    private readonly List<float> _speed = [];
    private readonly List<float> _position = [];
    private readonly List<CarType> _type = [];
    private readonly List<long> _claimedAt = [];
    private readonly List<int> _bay = [];

    public int ParkedCount { get; private set; }

    public int Add(float position, float speed, CarType type)
    {
        _position.Add(position);
        _speed.Add(speed);
        _type.Add(type);
        _claimedAt.Add(-1);
        _bay.Add(-1);
        return _position.Count - 1;
    }

    public int Count => _position.Count;

    public float Position(int car) => _position[car];

    /// <summary>Whether <paramref name="car"/> may claim the bay at <paramref name="at"/>: no other car is about to run through it.</summary>
    public bool CanClaim(int car, float at)
    {
        for (var other = 0; other < _position.Count; other++)
        {
            if (other != car && _position[other] <= at && !StopsShortOf(other, at))
                return false;
        }

        return true;
    }

    public void Claim(int car, int bay, long tick)
    {
        _bay[car] = bay;
        _claimedAt[car] = tick;
    }

    /// <summary>Whether a car that claimed a bay has waited too long for it and gives it up.</summary>
    public bool GivesUpClaim(int car, long tick) =>
        _claimedAt[car] >= 0 && tick - _claimedAt[car] > Clock.Ticks(ClaimGiveUpSeconds);

    /// <summary>Whether a parked car waiting to pull out has waited so long it gives up and stays.</summary>
    public bool GivesUpPullOut(int car, long waitingSince, long tick) =>
        tick - waitingSince > Clock.Ticks(PullOutGiveUpSeconds) && _bay[car] >= 0;

    /// <summary>Whether a parked car may pull out at <paramref name="at"/>: the car behind, if any, can stop short of it.</summary>
    public bool CanPullOut(int behind, float at) => behind < 0 || StopsShortOf(behind, at);

    /// <summary>Where a car that must stop before <paramref name="hold"/> starts braking.</summary>
    public float BrakeFrom(int car, float hold) => hold - StopDistance(car) - 1f;

    public void Park(int car)
    {
        _claimedAt[car] = -1;
        ParkedCount++;
    }

    /// <summary>Whether <paramref name="car"/>, braking now, stands a safe gap short of <paramref name="at"/>.</summary>
    private bool StopsShortOf(int car, float at) => _position[car] + StopDistance(car) + MinGap < at;

    /// <summary>How far <paramref name="car"/> runs braking as it normally does, metres.</summary>
    private float StopDistance(int car) => _speed[car] * _speed[car] / (2f * _braking[(int)_type[car]]);
}
