using System.Numerics;
using Harbor.Sim;

namespace Harbor.Game;

/// <summary>Draws the quay: each berth as a band, green where the selected ship would float, and the ships tied up.</summary>
public static class QuayView
{
    private const string ShipIcon = "assets/icons/ship.svg";

    public static void Draw(Canvas canvas, Port port, Ship? selected)
    {
        foreach (var berth in port.Berths)
        {
            // Green when the selected ship has water under its keel here when it is due.
            var safe = selected is null || berth.Depth + port.Tide.LevelAt(selected.Eta) - selected.Draught >= 0f;
            canvas.Band(berth.Start, berth.Start + berth.Length, safe);
        }

        foreach (var slot in port.Plan().Slots)
            canvas.Icon(ShipIcon, new Vector2(port.Berths[slot.Berth].Start, 0f));
    }
}
