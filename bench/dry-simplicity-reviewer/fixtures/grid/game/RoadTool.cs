using Grid.Sim;

namespace Grid.Game;

/// <summary>The road build tool: the class, level and shape of the next road, and the rules between them. The host calls Build on a placement.</summary>
public sealed class RoadTool(Simulation sim)
{
    public RoadClass Class { get; private set; } = RoadClass.Street;

    public int Level { get; private set; }

    public string Shape { get; private set; } = "Straight";

    /// <summary>Picks a class; a lane is only ever built on the ground.</summary>
    public void SetClass(RoadClass roadClass)
    {
        Class = roadClass;
        if (roadClass == RoadClass.Lane)
            Level = 0;
    }

    /// <summary>Raises or lowers the next road a level, within what can be built; a lane stays on the ground.</summary>
    public void SetLevel(int level) => Level = Class == RoadClass.Lane ? 0 : Math.Clamp(level, Levels.Lowest, Levels.Highest);

    public void SetShape(string shape) => Shape = shape;

    public Road Build(float length, int from, int to) => sim.Network.Add(Class, length, Level, from, to);
}
