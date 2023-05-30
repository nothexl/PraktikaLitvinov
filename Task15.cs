using System;
using System.Collections.Generic;

/* Дан массив строк words. Ваша задача - сгруппировать все анаграммы в массивы. Анаграммы - это слова, составленные из одних и тех же букв, но в разном порядке. */

class Program
{
    static List<List<string>> GroupAnagrams(string[] words)
    {
        Dictionary<string, List<string>> anagramGroups = new Dictionary<string, List<string>>();

        foreach (string word in words)
        {
            char[] characters = word.ToCharArray();
            Array.Sort(characters);
            string sortedWord = new string(characters);

            if (anagramGroups.ContainsKey(sortedWord))
            {
                anagramGroups[sortedWord].Add(word);
            }
            else
            {
                anagramGroups[sortedWord] = new List<string> { word };
            }
        }

        return new List<List<string>>(anagramGroups.Values);
    }

    static void Main()
    {
        string[] words = { "eat", "tea", "tan", "ate", "nat", "bat" };
        List<List<string>> anagramGroups = GroupAnagrams(words);

        foreach (List<string> group in anagramGroups)
        {
            Console.WriteLine(string.Join(", ", group));
        }
    }
}
