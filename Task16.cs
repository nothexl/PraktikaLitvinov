using System;

/* Дан массив целых чисел nums. Ваша задача - найти непрерывный подмассив (подотрезок) массива nums, который имеет наибольшую сумму чисел, и вернуть эту сумму. */

class Program
{
    static int MaxSubarraySum(int[] nums)
    {
        int currentSum = nums[0];
        int maxSum = nums[0];

        for (int i = 1; i < nums.Length; i++)
        {
            currentSum = Math.Max(nums[i], currentSum + nums[i]);
            maxSum = Math.Max(maxSum, currentSum);
        }

        return maxSum;
    }

    static void Main()
    {
        int[] nums = { -2, 1, -3, 4, -1, 2, 1, -5, 4 };
        int maxSum = MaxSubarraySum(nums);

        Console.WriteLine("Наибольшая сумма непрерывного подмассива: " + maxSum);
    }
}
