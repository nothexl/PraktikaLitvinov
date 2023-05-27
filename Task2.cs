using System;

/* Напишите программу, которая находит наибольшую общую подпоследовательность (LCS) для двух заданных строк. 
 * Общая подпоследовательность - это последовательность символов, которая присутствует в обеих строках в том же порядке, но не обязательно подряд.*/

class Program
{
    static string LongestCommonSubsequence(string text1, string text2)
    {
        int m = text1.Length;
        int n = text2.Length;

        int[,] dp = new int[m + 1, n + 1];

        for (int i = 1; i <= m; i++)
        {
            for (int j = 1; j <= n; j++)
            {
                if (text1[i - 1] == text2[j - 1])
                    dp[i, j] = dp[i - 1, j - 1] + 1;
                else
                    dp[i, j] = Math.Max(dp[i - 1, j], dp[i, j - 1]);
            }
        }

        int length = dp[m, n];
        char[] lcs = new char[length];
        int index = length - 1;
        int p = m, q = n;

        while (p > 0 && q > 0)
        {
            if (text1[p - 1] == text2[q - 1])
            {
                lcs[index] = text1[p - 1];
                index--;
                p--;
                q--;
            }
            else if (dp[p - 1, q] > dp[p, q - 1])
                p--;
            else
                q--;
        }

        return new string(lcs);
    }

    static void Main()
    {
        string text1 = Console.ReadLine();
        string text2 = Console.ReadLine();
        string lcs = LongestCommonSubsequence(text1, text2);

        Console.WriteLine($"Наибольшая общая подпоследовательность: {lcs}");
    }
}
