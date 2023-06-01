using System;
using System.Collections.Generic;

/* Дана строка, состоящая из уникальных символов. Необходимо найти все возможные перестановки этой строки и вывести их в алфавитном порядке. */

class Program
{
    static List<string> GetPermutations(string str)
    {
        List<string> permutations = new List<string>();
        Permute(str.ToCharArray(), 0, str.Length - 1, permutations);
        permutations.Sort();
        return permutations;
    }

    static void Permute(char[] strArr, int left, int right, List<string> permutations)
    {
        if (left == right)
        {
            permutations.Add(new string(strArr));
        }
        else
        {
            for (int i = left; i <= right; i++)
            {
                Swap(ref strArr[left], ref strArr[i]);
                Permute(strArr, left + 1, right, permutations);
                Swap(ref strArr[left], ref strArr[i]);
            }
        }
    }

    static void Swap(ref char a, ref char b)
    {
        char temp = a;
        a = b;
        b = temp;
    }

    static void Main()
    {
        string str = Console.ReadLine();
        List<string> permutations = GetPermutations(str);
        Console.WriteLine("Перестановки строки:");
        foreach (string permutation in permutations)
        {
            Console.WriteLine(permutation);
        }
    }
}
