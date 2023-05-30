using System;

/* Дана строка, содержащая только целые числа, разделенные запятыми. Ваша задача - найти подстроку (последовательность чисел), которая имеет максимальную сумму чисел. Верните сумму этой подстроки. */

class Program
{
    static int FindMaxSubarraySum(string input)
    {
        string[] numbers = input.Split(',');
        int maxSum = int.MinValue;
        int currentSum = 0;

        foreach (string number in numbers)
        {
            int num = int.Parse(number.Trim());
            currentSum = Math.Max(num, currentSum + num);
            maxSum = Math.Max(maxSum, currentSum);
        }

        return maxSum;
    }

    static void Main()
    {
        string input = "1, -2, 3, 4, -5, 6";
        int maxSum = FindMaxSubarraySum(input);

        Console.WriteLine("Ответ: " + maxSum);
    }
}
