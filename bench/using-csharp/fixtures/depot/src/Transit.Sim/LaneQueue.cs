namespace Transit.Sim;

/// <summary>The cars queued on each lane, as a doubly linked list from head to tail.</summary>
public sealed class LaneQueue(int lanes, int cars)
{
    public const int None = -1;

    private readonly int[] _head = Enumerable.Repeat(None, lanes).ToArray();
    private readonly int[] _tail = Enumerable.Repeat(None, lanes).ToArray();
    private readonly int[] _ahead = Enumerable.Repeat(None, cars).ToArray();
    private readonly int[] _behind = Enumerable.Repeat(None, cars).ToArray();

    public int Head(int lane) => _head[lane];

    /// <summary>Puts a car at the tail of a lane.</summary>
    public void Join(int car, int lane) => Link(car, lane, _tail[lane], None);

    /// <summary>Puts a car back at the head of the lane it just left.</summary>
    public void JoinAtHead(int car, int lane) => Link(car, lane, None, _head[lane]);

    /// <summary>Takes a car out of its lane, wherever it is in the queue.</summary>
    public void Leave(int car, int lane)
    {
        var (ahead, behind) = (_ahead[car], _behind[car]);
        if (ahead != None)
            _behind[ahead] = behind;
        else
            _head[lane] = behind;
        if (behind != None)
            _ahead[behind] = ahead;
        else
            _tail[lane] = ahead;
        _ahead[car] = _behind[car] = None;
    }

    /// <summary>Links a car into a lane between <paramref name="ahead"/> and <paramref name="behind"/>, either of them None at an end.</summary>
    private void Link(int car, int lane, int ahead, int behind)
    {
        _ahead[car] = ahead;
        _behind[car] = behind;
        if (ahead != None)
            _behind[ahead] = car;
        else
            _head[lane] = car;
        if (behind != None)
            _ahead[behind] = car;
        else
            _tail[lane] = car;
    }
}
