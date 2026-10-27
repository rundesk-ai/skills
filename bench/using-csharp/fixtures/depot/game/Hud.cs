using System.Globalization;
using Transit.Sim;

namespace Transit.Game;

/// <summary>The readout along the top of the screen, and the panel for the van the player selected.</summary>
public static class Hud
{
    public static void Draw(Canvas canvas, SimSnapshot snapshot)
    {
        var minutes = snapshot.Tick / Clock.TicksPerSecond / 60;
        canvas.Label(string.Create(CultureInfo.CurrentCulture, $"{minutes / 60:00}:{minutes % 60:00}"));
        canvas.Label(string.Create(CultureInfo.CurrentCulture, $"Vans {snapshot.VanCount}"));
        canvas.Label(string.Create(CultureInfo.CurrentCulture, $"Parked {snapshot.ParkedCars}"));
        canvas.Label(string.Create(CultureInfo.CurrentCulture, $"Trips {snapshot.TripsStarted}"));
    }

    public static void DrawVan(Canvas canvas, VanSystem vans, int van, int route)
    {
        canvas.Label(string.Create(CultureInfo.CurrentCulture, $"{vans.Speed(van) * 3.6f:0} km/h at {vans.Position(van):0} m"));
        canvas.Label(string.Create(CultureInfo.CurrentCulture, $"Round trip {vans.RoundTripSeconds(route) / 60f:0.0} min"));
        canvas.Label(string.Create(CultureInfo.CurrentCulture, $"Waiting {vans.WaitingOn(route)} parcels"));
    }
}
