using System;

/* У вас есть массив целых чисел. Ваша задача - найти такую непрерывную подпоследовательность элементов в массиве, чтобы сумма элементов была максимальной, при условии,
 * что в выбранной подпоследовательности не может быть двух смежных элементов. */

class Program
{
    static int MaxSumWithoutAdjacent(int[] nums)
    {
        int n = nums.Length;

        if (n == 0)
            return 0;
        if (n == 1)
            return nums[0];

        int[] dp = new int[n];
        dp[0] = nums[0];
        dp[1] = Math.Max(nums[0], nums[1]);

        for (int i = 2; i < n; i++)
        {
            dp[i] = Math.Max(nums[i] + dp[i - 2], dp[i - 1]);
        }

        return dp[n - 1];
    }

    static void Main()
    {
        int[] nums = { 1, 2, 3, 1 };
        int maxSum = MaxSumWithoutAdjacent(nums);
        Console.WriteLine("Максимальная сумма подпоследовательности без смежных элементов: " + maxSum);
    }
}
