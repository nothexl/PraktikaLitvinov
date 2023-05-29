using System;

/* Напишите программу, которая находит наибольший прямоугольник, состоящий из единиц, в заданной бинарной матрице. Прямоугольник должен быть выровнен с осями координат. */

class Program
{
    static int LargestRectangleArea(int[] heights)
    {
        int n = heights.Length;
        int[] left = new int[n];
        int[] right = new int[n];

        Stack<int> stack = new Stack<int>();

        for (int i = 0; i < n; i++)
        {
            while (stack.Count > 0 && heights[stack.Peek()] >= heights[i])
            {
                stack.Pop();
            }

            left[i] = stack.Count == 0 ? 0 : stack.Peek() + 1;
            stack.Push(i);
        }

        stack.Clear();

        for (int i = n - 1; i >= 0; i--)
        {
            while (stack.Count > 0 && heights[stack.Peek()] >= heights[i])
            {
                stack.Pop();
            }

            right[i] = stack.Count == 0 ? n : stack.Peek();
            stack.Push(i);
        }

        int maxArea = 0;

        for (int i = 0; i < n; i++)
        {
            int area = heights[i] * (right[i] - left[i]);
            maxArea = Math.Max(maxArea, area);
        }

        return maxArea;
    }

    static int LargestRectangleMatrix(int[,] matrix)
    {
        int rows = matrix.GetLength(0);
        int cols = matrix.GetLength(1);
        int maxArea = 0;
        int[] heights = new int[cols];

        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < cols; j++)
            {
                if (matrix[i, j] == 0)
                {
                    heights[j] = 0;
                }
                else
                {
                    heights[j] += matrix[i, j];
                }
            }

            int area = LargestRectangleArea(heights);
            maxArea = Math.Max(maxArea, area);
        }

        return maxArea;
    }

    static void Main()
    {
        int[,] matrix = {
            { 1, 0, 1, 0, 0 },
            { 1, 1, 1, 1, 1 },
            { 0, 1, 1, 1, 0 },
            { 1, 1, 0, 1, 1 }
        };

        int largestArea = LargestRectangleMatrix(matrix);
        Console.WriteLine($"Наибольшая прямоугольная область: {largestArea}");
    }
}
