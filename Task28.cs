using System;

/* Дано множество предметов с их весами и стоимостями, а также вместимость рюкзака.
 * Необходимо определить максимальную стоимость предметов, которую можно унести в рюкзаке без превышения его вместимости. */

public class KnapsackProblem
{
    public class Item
    {
        public int Weight { get; set; }
        public int Value { get; set; }
    }

    public static int SolveKnapsack(Item[] items, int capacity)
    {
        int[,] dp = new int[items.Length + 1, capacity + 1];

        for (int i = 1; i <= items.Length; i++)
        {
            for (int j = 1; j <= capacity; j++)
            {
                if (items[i - 1].Weight <= j)
                {
                    dp[i, j] = Math.Max(items[i - 1].Value + dp[i - 1, j - items[i - 1].Weight], dp[i - 1, j]);
                }
                else
                {
                    dp[i, j] = dp[i - 1, j];
                }
            }
        }

        return dp[items.Length, capacity];
    }

    public static void Main(string[] args)
    {
        Item[] items = new Item[]
        {
            new Item { Weight = 2, Value = 6 },
            new Item { Weight = 2, Value = 10 },
            new Item { Weight = 3, Value = 12 }
        };

        int capacity = 5;
        int maxTotalValue = SolveKnapsack(items, capacity);
        Console.WriteLine(maxTotalValue);
    }
}
