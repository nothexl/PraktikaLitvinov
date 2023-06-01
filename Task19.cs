using System;

/* У вас есть массив целых чисел и два ограничения: k1 и k2. Ваша задача - найти такую непрерывную подпоследовательность элементов в массиве, чтобы сумма элементов была максимальной,
 * но не превышала значение k2. При этом, сумма элементов должна быть больше или равна значению k1. */

class Program
{
    static int MaxSumSubarrayWithConstraints(int[] nums, int k1, int k2)
    {
        int n = nums.Length;

        if (n == 0)
            return 0;

        int maxSum = int.MinValue;
        int currentSum = 0;

        for (int i = 0; i < n; i++)
        {
            currentSum = Math.Max(nums[i], currentSum + nums[i]);

            if (currentSum >= k1 && currentSum <= k2)
            {
                maxSum = Math.Max(maxSum, currentSum);
            }
            else if (currentSum < 0)
            {
                currentSum = 0;
            }
        }

        return maxSum;
    }

    static void Main()
    {
        int[] nums = { 1, -2, 3, 10, -4, 7, 2, -5 };
        int k1 = 5;
        int k2 = 10;
        int maxSum = MaxSumSubarrayWithConstraints(nums, k1, k2);
        Console.WriteLine("Max sum of subarray with constraints: " + maxSum);
    }
}