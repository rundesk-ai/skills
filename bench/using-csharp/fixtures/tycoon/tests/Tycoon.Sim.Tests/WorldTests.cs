using Tycoon.Sim;

public class WorldTests
{
    static World Small(int seed)
    {
        var w = new World(seed);
        w.Add(Kind.Farm, 2);
        w.Add(Kind.Farm, 3);
        w.Add(Kind.Mill, 5);
        w.Add(Kind.Bakery, 9);
        w.Add(Kind.Shop, 12);
        w.Link();
        return w;
    }

    [Fact]
    public void SameSeedSameGame()
    {
        var a = Small(7);
        var b = Small(7);
        for (var i = 0; i < 200; i++) { a.Step(); b.Step(); }
        Assert.Equal(a.Digest(), b.Digest());
    }

    [Fact]
    public void TaxIsTenPercent()
    {
        Assert.Equal(10, Tax.Due(100, 0.1));
    }

    [Fact]
    public void SaveRoundTrips()
    {
        var w = Small(3);
        for (var i = 0; i < 20; i++) w.Step();
        var loaded = Save.Read(Save.Write(w), 3);
        Assert.Equal(w.Digest(), loaded.Digest());
    }
}
