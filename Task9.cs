using System;
using System.Collections.Generic;

/* Задача о поиске пары суммирующихся элементов. Дан массив целых чисел и целевое число. Вам нужно найти и вернуть индексы двух чисел в массиве, сумма которых равна целевому числу. */

class Program
{
    static int[] TwoSum(int[] nums, int target)
    {
        Dictionary<int, int> numIndexMap = new Dictionary<int, int>();

        for (int i = 0; i < nums.Length; i++)
        {
            int complement = target - nums[i];
            if (numIndexMap.ContainsKey(complement))
            {
                return new int[] { numIndexMap[complement], i };
            }
            numIndexMap[nums[i]] = i;
        }

        return null;
    }

    static void Main()
    {
        int[] nums = { 2, 7, 11, 15 };
        int target = 9;

        int[] result = TwoSum(nums, target);

        if (result != null)
        {
            Console.WriteLine("Индексы двух чисел: {0}, {1}", result[0], result[1]);
        }
        else
        {
            Console.WriteLine("Такие числа не найдены.");
        }
    }
}
