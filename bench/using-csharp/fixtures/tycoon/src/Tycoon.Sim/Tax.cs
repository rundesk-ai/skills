namespace Tycoon.Sim;

public static class Tax
{
    // rate is a fraction, e.g. 0.1 for ten per cent
    public static int Due(int revenue, double rate) => (int)Math.Round(revenue * rate);
}
