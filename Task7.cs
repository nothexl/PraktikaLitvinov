using System;

/* Напишите программу, которая находит наибольший квадратный подмассив в заданной бинарной матрице.
 * Квадратный подмассив - это подматрица, в которой все элементы равны 1. */

class Program
{
    static int LargestSquareSubmatrix(int[,] matrix)
    {
        int rows = matrix.GetLength(0);
        int cols = matrix.GetLength(1);
        int[,] dp = new int[rows, cols];
        int largestSize = 0;

        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                if (i == 0 || j == 0)
                {
                    dp[i, j] = matrix[i, j];
                }
                else
                {
                    if (matrix[i, j] == 1)
                    {
                        dp[i, j] = Math.Min(dp[i - 1, j - 1], Math.Min(dp[i - 1, j], dp[i, j - 1])) + 1;
                    }
                    else
                    {
                        dp[i, j] = 0;
                    }
                }

                largestSize = Math.Max(largestSize, dp[i, j]);
            }
        }

        return largestSize;
    }

    static void Main()
    {
        int[,] matrix = {
            { 1, 0, 1, 0, 0 },
            { 1, 1, 1, 1, 1 },
            { 0, 1, 1, 1, 0 },
            { 1, 1, 1, 1, 1 },
            { 0, 1, 1, 1, 0 }
        };

        int largestSize = LargestSquareSubmatrix(matrix);
        Console.WriteLine($"Наибольшай размер квадратного подмассива: {largestSize}");
    }
}
