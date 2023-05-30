using System;

/* Задача о наибольшей общей подстроке (Longest Common Substring). Даны две строки. Вам нужно найти наибольшую общую подстроку (самую длинную подстроку, которая встречается в обеих строках). */

class Program
{
    static string LongestCommonSubstring(string str1, string str2)
    {
        int[,] lengths = new int[str1.Length + 1, str2.Length + 1];
        int maxLength = 0;
        int endIndex = 0;

        for (int i = 1; i <= str1.Length; i++)
        {
            for (int j = 1; j <= str2.Length; j++)
            {
                if (str1[i - 1] == str2[j - 1])
                {
                    lengths[i, j] = lengths[i - 1, j - 1] + 1;

                    if (lengths[i, j] > maxLength)
                    {
                        maxLength = lengths[i, j];
                        endIndex = i - 1;
                    }
                }
                else
                {
                    lengths[i, j] = 0;
                }
            }
        }

        return str1.Substring(endIndex - maxLength + 1, maxLength);
    }

    static void Main()
    {
        string str1 = "abcdefg";
        string str2 = "bcdekl";

        string longestCommonSubstring = LongestCommonSubstring(str1, str2);

        Console.WriteLine("Наибольшая общая подстрока: " + longestCommonSubstring);
    }
}
