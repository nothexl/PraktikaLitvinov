using System;

/* Даны две строки. Необходимо найти длину наибольшей общей подстроки этих строк.
 * Общая подстрока - это последовательность символов, которая встречается в обеих строках и не обязательно расположена в одной и той же позиции. */

class Program
{
    static int FindLongestCommonSubstringLength(string str1, string str2)
    {
        int[,] dp = new int[str1.Length + 1, str2.Length + 1];
        int maxLength = 0;

        for (int i = 1; i <= str1.Length; i++)
        {
            for (int j = 1; j <= str2.Length; j++)
            {
                if (str1[i - 1] == str2[j - 1])
                {
                    dp[i, j] = dp[i - 1, j - 1] + 1;
                    maxLength = Math.Max(maxLength, dp[i, j]);
                }
            }
        }

        return maxLength;
    }

    static void Main()
    {
        string str1 = Console.ReadLine();
        string str2 = Console.ReadLine();
        int longestSubstringLength = FindLongestCommonSubstringLength(str1, str2);
        Console.WriteLine("Длина наибольшей общей подстроки: " + longestSubstringLength);
    }
}