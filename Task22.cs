using System;

/* Дана строка. Необходимо найти палиндромную подстроку максимальной длины в этой строке и вернуть ее.
 * Палиндром - это строка, которая читается одинаково вперед и назад. */

class Program
{
    static string FindLongestPalindromeSubstring(string input)
    {
        int n = input.Length;
        bool[,] dp = new bool[n, n];
        string longestPalindrome = "";

        for (int len = 1; len <= n; len++)
        {
            for (int start = 0; start <= n - len; start++)
            {
                int end = start + len - 1;

                if (input[start] == input[end])
                {
                    if (len <= 2 || dp[start + 1, end - 1])
                    {
                        dp[start, end] = true;
                        if (len > longestPalindrome.Length)
                            longestPalindrome = input.Substring(start, len);
                    }
                }
            }
        }

        return longestPalindrome;
    }

    static void Main()
    {
        string input = "babad";
        string longestPalindrome = FindLongestPalindromeSubstring(input);
        Console.WriteLine("Максимальная палиндромная подстрока: " + longestPalindrome);
    }
}
