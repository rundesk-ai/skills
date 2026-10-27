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
            if (other == car || _position[other] > at)
                continue;
            var speed = _speed[other];
            if (_position[other] + (speed * speed / (2f * _braking[(int)_type[other]])) + MinGap > at)
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
        _claimedAt[car] >= 0 && tick - _claimedAt[car] > (long)(ClaimGiveUpSeconds * Clock.TicksPerSecond);

    /// <summary>Whether a parked car waiting to pull out has waited so long it gives up and stays.</summary>
    public bool GivesUpPullOut(int car, long waitingSince, long tick) =>
        tick - waitingSince > (long)(PullOutGiveUpSeconds * Clock.TicksPerSecond) && _bay[car] >= 0;

    /// <summary>Whether a parked car may pull out at <paramref name="at"/>: the car behind can stop short of it.</summary>
    public bool CanPullOut(int behind, float at)
    {
        if (behind < 0)
            return true;
        var speed = _speed[behind];
        return _position[behind] + (speed * speed / (2f * _braking[(int)_type[behind]])) + MinGap < at;
    }

    /// <summary>Where a car that must stop before <paramref name="hold"/> starts braking.</summary>
    public float BrakeFrom(int car, float hold)
    {
        var stopping = (_speed[car] * _speed[car] / (2f * _braking[(int)_type[car]])) + 1f;
        return hold - stopping;
    }

    public void Park(int car)
    {
        _claimedAt[car] = -1;
        ParkedCount++;
    }
}
