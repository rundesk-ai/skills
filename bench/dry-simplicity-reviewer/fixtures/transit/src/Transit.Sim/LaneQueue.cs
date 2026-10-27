namespace Transit.Sim;

/// <summary>The cars queued on each lane, as a doubly linked list from head to tail.</summary>
public sealed class LaneQueue(int lanes, int cars)
{
    public const int None = -1;

    private readonly int[] _head = Enumerable.Repeat(None, lanes).ToArray();
    private readonly int[] _tail = Enumerable.Repeat(None, lanes).ToArray();
    private readonly int[] _ahead = Enumerable.Repeat(None, cars).ToArray();
    private readonly int[] _behind = Enumerable.Repeat(None, cars).ToArray();

    public int Lanes => lanes;

    public int Head(int lane) => _head[lane];

    public int Behind(int car) => _behind[car];

    /// <summary>Puts a car at the tail of a lane.</summary>
    public void Join(int car, int lane)
    {
        var tail = _tail[lane];
        _ahead[car] = tail;
        _behind[car] = None;
        if (tail != None)
            _behind[tail] = car;
        else
            _head[lane] = car;
        _tail[lane] = car;
    }

    /// <summary>Puts a car back at the head of the lane it just left.</summary>
    public void JoinAtHead(int car, int lane)
    {
        var head = _head[lane];
        _ahead[car] = None;
        _behind[car] = head;
        if (head != None)
            _ahead[head] = car;
        else
            _tail[lane] = car;
        _head[lane] = car;
    }

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
}
