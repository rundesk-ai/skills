using System.Text;

namespace Tycoon.Sim;

public class World
{
    public readonly Dictionary<int, Business> Businesses = new();
    public readonly Dictionary<int, Job> Jobs = new();
    public readonly List<string> Log = new();
    public double TaxRate = 0.1;
    public int Tick;
    public Random Rng;
    int _nextJob;

    public World(int seed) { Rng = new Random(seed); }

    public Business Add(Kind kind, int price)
    {
        var b = new Business(Businesses.Count + 1, kind, price);
        Businesses[b.Id] = b;
        return b;
    }

    public void Link()
    {
        foreach (var b in Businesses.Values)
        {
            var wanted = b.Kind switch { Kind.Mill => Kind.Farm, Kind.Bakery => Kind.Mill, Kind.Shop => Kind.Bakery, _ => (Kind?)null };
            if (wanted == null) continue;
            b.SupplierId = Businesses.Values.Where(s => s.Kind == wanted).OrderBy(s => s.Price).First().Id;
        }
    }

    public void Step()
    {
        Tick++;

        // Production and orders.
        foreach (var b in Businesses.Values.ToList())
        {
            if (b.Kind == Kind.Farm)
                b.Stock += Rng.Next(1, 4);
            else if (b.SupplierId is int s)
                Jobs[_nextJob++] = new Job(b.Id, Rng.Next(0, 3), Rng.Next(1, 5));
        }

        // Fulfil the most urgent jobs first.
        var queue = Jobs.Values.ToList();
        queue.Sort((x, y) => y.Priority.CompareTo(x.Priority));
        var done = new List<int>();
        foreach (var job in queue)
        {
            var buyer = Businesses[job.BusinessId];
            var seller = Businesses.Values.First(x => x.Id == buyer.SupplierId);
            var amount = Math.Min(job.Amount, seller.Stock);
            if (amount == 0) continue;
            var revenue = amount * seller.Price;
            seller.Stock -= amount;
            seller.Cash += revenue - Tax.Due(revenue, TaxRate);
            buyer.Cash -= revenue;
            buyer.Stock += amount;
            Log.Add($"t{Tick}: {seller.Kind} {seller.Id} sold {amount} to {buyer.Id} for {revenue}");
            done.Add(Jobs.First(kv => kv.Value == job).Key);
        }
        foreach (var id in done) Jobs.Remove(id);

        // Shops sell to the public.
        foreach (var shop in Businesses.Values.Where(x => x.Kind == Kind.Shop))
        {
            var sold = Math.Min(shop.Stock, Rng.Next(0, 6));
            shop.Stock -= sold;
            shop.Cash += sold * shop.Price * 3;
        }
    }

    public string Digest()
    {
        var sb = new StringBuilder();
        foreach (var b in Businesses.Values.OrderBy(b => b.Id))
            sb.Append(b.Id).Append(':').Append(b.Stock).Append(':').Append(b.Cash).Append(';');
        return sb.ToString();
    }
}
