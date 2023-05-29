using System;

/* Напишите программу, которая находит наибольшую возрастающую подматрицу в заданной матрице целых чисел.
 * Наибольшая возрастающая подматрица - это подматрица, в которой значения элементов упорядочены в возрастающем порядке, и она имеет наибольшую площадь среди всех возможных подматриц. */

class Program
{
    static int LargestIncreasingSubmatrix(int[,] matrix)
    {
        int rows = matrix.GetLength(0);
        int cols = matrix.GetLength(1);
        int[,] dp = new int[rows, cols];
        int largestArea = 0;

        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                if (i == 0 || j == 0)
                {
                    dp[i, j] = 1;
                }
                else
                {
                    if (matrix[i, j] > matrix[i - 1, j] && matrix[i, j] > matrix[i, j - 1])
                    {
                        dp[i, j] = Math.Min(dp[i - 1, j - 1], Math.Min(dp[i - 1, j], dp[i, j - 1])) + 1;
                    }
                    else
                    {
                        dp[i, j] = 1;
                    }
                }

                largestArea = Math.Max(largestArea, dp[i, j]);
            }
        }

        return largestArea;
    }

    static void Main()
    {
        int[,] matrix = {
            { 1, 3, 2, 4 },
            { 2, 4, 7, 5 },
            { 3, 1, 6, 8 }
        };

        int largestArea = LargestIncreasingSubmatrix(matrix);
        Console.WriteLine($"Наибольшая возрастающая подматрица: {largestArea}");
    }
}
