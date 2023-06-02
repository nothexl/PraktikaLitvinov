using System;

/* Даны две строки. Редакционное расстояние между строками - это минимальное количество операций (вставка, удаление, замена символа),
 * необходимых для преобразования одной строки в другую. Найдите редакционное расстояние между двумя заданными строками. */

class Program
{
    static int EditDistance(string str1, string str2)
    {
        int m = str1.Length;
        int n = str2.Length;

        int[,] dp = new int[m + 1, n + 1];

        for (int i = 0; i <= m; i++)
        {
            for (int j = 0; j <= n; j++)
            {
                if (i == 0)
                {
                    dp[i, j] = j;
                }
                else if (j == 0)
                {
                    dp[i, j] = i;
                }
                else if (str1[i - 1] == str2[j - 1])
                {
                    dp[i, j] = dp[i - 1, j - 1];
                }
                else
                {
                    dp[i, j] = 1 + Math.Min(dp[i, j - 1], Math.Min(dp[i - 1, j], dp[i - 1, j - 1]));
                }
            }
        }

        return dp[m, n];
    }

    static void Main()
    {
        string str1 = "kitten";
        string str2 = "sitting";

        int editDistance = EditDistance(str1, str2);

        Console.WriteLine("Редакционное расстояние между строками " + str1 + " и " + str2 + ": " + editDistance);
    }
}
