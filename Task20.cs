using System;

/* Дан массив целых чисел. Необходимо найти непрерывный подмассив этого массива, у которого сумма элементов является максимальной, и вернуть эту максимальную сумму. */

class Program
{
    static int FindMaxSubarraySum(int[] nums)
    {
        int n = nums.Length;
        int currentSum = nums[0];
        int maxSum = nums[0];

        for (int i = 1; i < n; i++)
        {
            currentSum = Math.Max(nums[i], currentSum + nums[i]);
            maxSum = Math.Max(maxSum, currentSum);
        }

        return maxSum;
    }

    static void Main()
    {
        int[] nums = { 1, -2, 3, 10, -4, 7, 2, -5 };
        int maxSum = FindMaxSubarraySum(nums);
        Console.WriteLine("Максимальная сумма подмассива: " + maxSum);
    }
}
