using System;

/* Дана шахматная доска размером NxN. Необходимо расставить на ней N ферзей таким образом, чтобы они не били друг друга (не находились на одной вертикали, горизонтали или диагонали).
 * Необходимо найти хотя бы одно корректное решение или определить, что такого решения не существует. */

public class QueenPlacementProblem
{
    private int size;
    private int[,] board;

    public QueenPlacementProblem(int size)
    {
        this.size = size;
        this.board = new int[size, size];
    }

    public void Solve()
    {
        if (PlaceQueens(0))
        {
            PrintBoard();
        }
        else
        {
            Console.WriteLine("No solution found.");
        }
    }

    private bool PlaceQueens(int col)
    {
        if (col >= size)
        {
            return true;
        }

        for (int row = 0; row < size; row++)
        {
            if (IsSafe(row, col))
            {
                board[row, col] = 1;

                if (PlaceQueens(col + 1))
                {
                    return true;
                }

                board[row, col] = 0;
            }
        }

        return false;
    }

    private bool IsSafe(int row, int col)
    {
        for (int i = 0; i < col; i++)
        {
            if (board[row, i] == 1)
            {
                return false;
            }
        }

        for (int i = row, j = col; i >= 0 && j >= 0; i--, j--)
        {
            if (board[i, j] == 1)
            {
                return false;
            }
        }

        for (int i = row, j = col; i < size && j >= 0; i++, j--)
        {
            if (board[i, j] == 1)
            {
                return false;
            }
        }

        return true;
    }

    private void PrintBoard()
    {
        for (int i = 0; i < size; i++)
        {
            for (int j = 0; j < size; j++)
            {
                Console.Write(board[i, j] + " ");
            }
            Console.WriteLine();
        }
    }

    public static void Main(string[] args)
    {
        int size = 8;
        QueenPlacementProblem problem = new QueenPlacementProblem(size);
        problem.Solve();
    }
}
