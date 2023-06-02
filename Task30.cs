using System;
using System.Collections.Generic;

/* Дана строка и словарь, содержащий список допустимых слов. Необходимо определить, можно ли разбить данную строку на последовательность слов из словаря.
 * Если это возможно, то вернуть список слов, на которые можно разбить строку, в противном случае вернуть пустой список. */

public class WordBreakProblem
{
    public static List<string> WordBreak(string s, HashSet<string> wordDict)
    {
        List<string>[] dp = new List<string>[s.Length + 1];
        dp[0] = new List<string>();

        for (int i = 0; i <= s.Length; i++)
        {
            if (dp[i] == null)
            {
                continue;
            }

            for (int j = i + 1; j <= s.Length; j++)
            {
                string word = s.Substring(i, j - i);
                if (wordDict.Contains(word))
                {
                    if (dp[j] == null)
                    {
                        dp[j] = new List<string>();
                    }

                    dp[j].Add(word);
                }
            }
        }

        if (dp[s.Length] == null)
        {
            return new List<string>();
        }

        List<string> result = new List<string>();
        ConstructWordBreakResult(dp, s.Length, result, "");
        return result;
    }

    private static void ConstructWordBreakResult(List<string>[] dp, int index, List<string> result, string current)
    {
        if (index == 0)
        {
            result.Add(current.Trim());
            return;
        }

        foreach (string word in dp[index])
        {
            ConstructWordBreakResult(dp, index - word.Length, result, word + " " + current);
        }
    }

    public static void Main(string[] args)
    {
        string s = "applepie";
        HashSet<string> wordDict = new HashSet<string> { "apple", "pie" };
        List<string> wordBreakResult = WordBreak(s, wordDict);

        if (wordBreakResult.Count > 0)
        {
            Console.WriteLine("Возможное разбиение:");
            foreach (string word in wordBreakResult)
            {
                Console.WriteLine(word);
            }
        }
        else
        {
            Console.WriteLine("Строка не может быть разбита на слова.");
        }
    }
}
