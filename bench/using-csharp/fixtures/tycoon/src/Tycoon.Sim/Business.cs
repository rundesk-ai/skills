namespace Tycoon.Sim;

public enum Kind { Farm, Mill, Bakery, Shop }

public class Business
{
    public int Id;
    public Kind Kind;
    public int Stock;
    public int Price;          // dollars per unit
    public int Cash;           // dollars
    public int? SupplierId;

    public Business(int id, Kind kind, int price)
    {
        Id = id;
        Kind = kind;
        Price = price;
    }
}

public record Job(int BusinessId, int Priority, int Amount);
