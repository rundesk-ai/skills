using System.Text;

namespace Tycoon.Sim;

// A plain text save: one line per record.
public static class Save
{
    public static string Write(World w)
    {
        var sb = new StringBuilder();
        sb.AppendLine($"world {w.Tick} {w.TaxRate}");
        foreach (var b in w.Businesses.Values)
            sb.AppendLine($"business {b.Id} {b.Kind} {b.Stock} {b.Price} {b.Cash} {b.SupplierId?.ToString() ?? "-"}");
        foreach (var (id, j) in w.Jobs)
            sb.AppendLine($"job {id} {j.BusinessId} {j.Priority} {j.Amount}");
        return sb.ToString();
    }

    public static World Read(string text, int seed)
    {
        var w = new World(seed);
        foreach (var line in text.Split('\n', StringSplitOptions.RemoveEmptyEntries))
        {
            var p = line.Trim().Split(' ');
            switch (p[0])
            {
                case "world":
                    w.Tick = int.Parse(p[1]);
                    w.TaxRate = double.Parse(p[2]);
                    break;
                case "business":
                    var b = new Business(int.Parse(p[1]), Enum.Parse<Kind>(p[2]), int.Parse(p[4]))
                    {
                        Stock = int.Parse(p[3]),
                        Cash = int.Parse(p[5]),
                        SupplierId = p[6] == "-" ? null : int.Parse(p[6]),
                    };
                    w.Businesses[b.Id] = b;
                    break;
                case "job":
                    w.Jobs[int.Parse(p[1])] = new Job(int.Parse(p[2]), int.Parse(p[3]), int.Parse(p[4]));
                    break;
            }
        }
        return w;
    }
}
