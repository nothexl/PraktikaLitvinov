using System;
using System.Collections.Generic;

/* Напишите программу, которая находит все неповторяющиеся элементы в заданном массиве целых чисел и возвращает их в новом массиве. */

class Program
{
    static int[] FindNonRepeatingElements(int[] nums)
    {
        Dictionary<int, int> frequencyMap = new Dictionary<int, int>();

        foreach (int num in nums)
        {
            if (frequencyMap.ContainsKey(num))
                frequencyMap[num]++;
            else
                frequencyMap[num] = 1;
        }

        List<int> nonRepeatingElements = new List<int>();
        foreach (KeyValuePair<int, int> kvp in frequencyMap)
        {
            if (kvp.Value == 1)
                nonRepeatingElements.Add(kvp.Key);
        }

        return nonRepeatingElements.ToArray();
    }

    static void Main()
    {

        Random random = new Random();
        int N = Convert.ToInt32(Console.ReadLine());
        int[] A = new int[N];
        for (int i = 0; i < N; i ++)
        {
            A[i] = random.Next(-10, 10);
        }

        Console.WriteLine("Массив: ");
        for (int i = 0; i < N; i++)
        {
            Console.Write($"{A[i]} ");
        }

        Console.WriteLine();
        Console.WriteLine("Неповторяющиеся элементы: ");
        int[] result = FindNonRepeatingElements(A);
        foreach (int num in result)
        {
            Console.Write(num + " ");
        }
    }
}
