using System;

/* Задача о наибольшей палиндромной подстроке (Longest Palindromic Substring). 
 * Дана строка. Вам нужно найти наибольшую палиндромную подстроку (самую длинную подстроку, которая читается одинаково в обоих направлениях). */

class Program
{
    static string LongestPalindromicSubstring(string str)
    {
        if (string.IsNullOrEmpty(str))
        {
            return str;
        }

        int start = 0;
        int maxLength = 1;

        for (int i = 0; i < str.Length; i++)
        {
            int len1 = ExpandAroundCenter(str, i, i);
            int len2 = ExpandAroundCenter(str, i, i + 1);
            int len = Math.Max(len1, len2);

            if (len > maxLength)
            {
                maxLength = len;
                start = i - (len - 1) / 2;
            }
        }

        return str.Substring(start, maxLength);
    }

    static int ExpandAroundCenter(string str, int left, int right)
    {
        while (left >= 0 && right < str.Length && str[left] == str[right])
        {
            left--;
            right++;
        }

        return right - left - 1;
    }

    static void Main()
    {
        string str = Console.ReadLine();
        string longestPalindromicSubstring = LongestPalindromicSubstring(str);
        Console.WriteLine("Наибольшая палиндромная подстрока: " + longestPalindromicSubstring);
    }
}
