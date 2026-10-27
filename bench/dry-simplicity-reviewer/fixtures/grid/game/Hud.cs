using System.Globalization;
using Grid.Sim;

namespace Grid.Game;

/// <summary>The build bar: buttons for the road tool, and a line saying what the next road will be. The host calls Press on a click.</summary>
public sealed class Hud(RoadTool tool)
{
    private RoadClass _class = RoadClass.Street;
    private int _level;
    private string _shape = "Straight";

    public List<string> Lines { get; } = [];

    /// <summary>Handles a build-bar button by its action name.</summary>
    public void Press(string action)
    {
        switch (action)
        {
            case "class_lane": _class = RoadClass.Lane; tool.SetClass(_class); break;
            case "class_local": _class = RoadClass.Local; tool.SetClass(_class); break;
            case "class_street": _class = RoadClass.Street; tool.SetClass(_class); break;
            case "class_avenue": _class = RoadClass.Avenue; tool.SetClass(_class); break;
            case "class_highway": _class = RoadClass.Highway; tool.SetClass(_class); break;
            case "level_up": _level = Math.Min(_level + 1, Levels.Highest); tool.SetLevel(_level); break;
            case "level_down": _level = Math.Max(_level - 1, Levels.Lowest); tool.SetLevel(_level); break;
            case "shape_straight": _shape = "Straight"; tool.SetShape(_shape); break;
            case "shape_curve": _shape = "Curve"; tool.SetShape(_shape); break;
        }
    }

    public void Draw() =>
        Lines.Add(string.Create(CultureInfo.InvariantCulture, $"Next road: {_class}, level {_level}, {_shape}"));
}
