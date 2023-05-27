using System;

/* Напишите программу, которая находит все перестановки заданного набора чисел. */

class Program
{
    static void Permute(int[] nums, int start, int end)
    {
        if (start == end)
        {
            PrintArray(nums);
        }
        else
        {
            for (int i = start; i <= end; i++)
            {
                Swap(nums, start, i);
                Permute(nums, start + 1, end);
                Swap(nums, start, i);
            }
        }
    }

    static void Swap(int[] nums, int i, int j)
    {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }

    static void PrintArray(int[] nums)
    {
        foreach (int num in nums)
        {
            Console.Write($"{num} ");
        }
        Console.WriteLine();
    }

    static void Main()
    {
        Random random = new Random();
        int N = Convert.ToInt32(Console.ReadLine());
        int[] A = new int[N];
        for (int i = 0; i < N; i++)
        {
            A[i] = random.Next(0, 9);
        }

        Console.WriteLine("Набор чисел:");
        for (int i = 0; i < N; i++)
        {
            Console.Write($"{A[i]} ");
        }

        Console.WriteLine();
        Console.WriteLine("Все перестановки:");
        Permute(A, 0, A.Length - 1);
    }
}