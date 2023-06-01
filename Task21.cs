using System;
using System.Collections.Generic;

/* Даны две строки str1 и str2, состоящие из строчных букв английского алфавита. 
 * Ваша задача - определить, можно ли переставить символы в строке str1, чтобы получить строку str2. При этом каждая перестановка должна быть уникальной. */

class Program
{
    static bool ArePermutations(string str1, string str2)
    {
        if (str1.Length != str2.Length)
            return false;

        Dictionary<char, int> charCount = new Dictionary<char, int>();

        foreach (char c in str1)
        {
            if (charCount.ContainsKey(c))
                charCount[c]++;
            else
                charCount[c] = 1;
        }

        foreach (char c in str2)
        {
            if (!charCount.ContainsKey(c) || charCount[c] == 0)
                return false;

            charCount[c]--;
        }

        return true;
    }

    static void Main()
    {
        string str1 = Console.ReadLine();
        string str2 = Console.ReadLine();

        bool arePermutations = ArePermutations(str1, str2);

        Console.WriteLine("Ответ: " + arePermutations);
    }
}
