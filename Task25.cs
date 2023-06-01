using System;
using System.Linq;

/* Даны две строки s1 и s2. Необходимо определить, является ли s2 перестановкой s1. То есть, можно ли переставить символы в s2 таким образом, чтобы получилась строка s1. */

class Program
{
    static bool IsPermutation(string s1, string s2)
    {
        if (s1.Length != s2.Length)
        {
            return false;
        }

        int[] count = new int[26];

        for (int i = 0; i < s1.Length; i++)
        {
            count[s1[i] - 'a']++;
            count[s2[i] - 'a']--;
        }

        return count.All(c => c == 0);
    }

    static void Main()
    {
        string s1 = "abc";
        string s2 = "bca";
        bool isPermutation = IsPermutation(s1, s2);
        Console.WriteLine("s2 является перестановкой s1: " + isPermutation);
    }
}
