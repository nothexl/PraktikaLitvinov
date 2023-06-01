using System;

/* Дан массив положительных и отрицательных целых чисел nums. Ваша задача - найти непрерывный подмассив (подстроку) массива nums такую, 
 * что произведение всех чисел в этом подмассиве является максимальным, и вернуть это максимальное произведение. */

class Program
{
    static int MaxSubarrayProduct(int[] nums)
    {
        int maxProduct = nums[0];
        int currentMax = nums[0];
        int currentMin = nums[0];

        for (int i = 1; i < nums.Length; i++)
        {
            int tempMax = currentMax;
            currentMax = Math.Max(Math.Max(nums[i], currentMax * nums[i]), currentMin * nums[i]);
            currentMin = Math.Min(Math.Min(nums[i], tempMax * nums[i]), currentMin * nums[i]);
            maxProduct = Math.Max(maxProduct, currentMax);
        }

        return maxProduct;
    }

    static void Main()
    {
        int[] nums = { 2, 3, -2, 4 };
        int maxProduct = MaxSubarrayProduct(nums);

        Console.WriteLine("Максимальное произведение подмассива: " + maxProduct);
    }
}
