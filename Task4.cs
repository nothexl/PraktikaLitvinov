using System;

/* Напишите программу, которая определяет, можно ли разделить заданный массив положительных целых чисел на две подмассива таким образом,
 * чтобы сумма элементов в каждом подмассиве была одинаковой. */

class Program
{
    static bool CanSplitArray(int[] nums)
    {
        int n = nums.Length;
        int totalSum = 0;

        foreach (int num in nums)
        {
            totalSum += num;
        }

        if (totalSum % 2 != 0)
        {
            return false;
        }

        int targetSum = totalSum / 2;
        bool[,] dp = new bool[n + 1, targetSum + 1];

        for (int i = 0; i <= n; i++)
        {
            dp[i, 0] = true;
        }

        for (int i = 1; i <= n; i++)
        {
            for (int j = 1; j <= targetSum; j++)
            {
                dp[i, j] = dp[i - 1, j];
                if (j >= nums[i - 1])
                {
                    dp[i, j] = dp[i, j] || dp[i - 1, j - nums[i - 1]];
                }
            }
        }

        return dp[n, targetSum];
    }

    static void Main()
    {
        Random random = new Random();
        int N = Convert.ToInt32(Console.ReadLine());
        int[] A = new int[N];
        for (int i = 0; i < N; i++)
        {
            A[i] = random.Next(0, 10);
        }

        Console.WriteLine("Массив: ");
        for (int i = 0; i < N; i++)
        {
            Console.Write($"{A[i]} ");
        }

        Console.WriteLine();
        bool canSplit = CanSplitArray(A);
        Console.WriteLine($"Можно ли разделить массив: {canSplit}");
    }
}
