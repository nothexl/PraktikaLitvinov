using System;

/* Напишите программу, которая находит наибольшую возрастающую подпоследовательность (LIS) в заданном массиве целых чисел.
 * Наибольшая возрастающая подпоследовательность - это подпоследовательность элементов массива, в которой числа упорядочены в возрастающем порядке,
 * и она имеет наибольшую длину среди всех возможных подпоследовательностей. */

class Program
{
    static int LongestIncreasingSubsequence(int[] nums)
    {
        int n = nums.Length;
        int[] dp = new int[n];

        for (int i = 0; i < n; i++)
        {
            dp[i] = 1;
            for (int j = 0; j < i; j++)
            {
                if (nums[i] > nums[j])
                    dp[i] = Math.Max(dp[i], dp[j] + 1);
            }
        }

        int maxLength = 0;
        for (int i = 0; i < n; i++)
        {
            maxLength = Math.Max(maxLength, dp[i]);
        }

        return maxLength;
    }

    static void Main()
    {
        int[] nums = { 10, 22, 9, 33, 21, 50, 41, 60 };
        int length = LongestIncreasingSubsequence(nums);

        Console.WriteLine($"Длина наибольшей возрастающей подпоследовательности: {length}");
    }
}
