using System;
using System.Text;

/* Задача о сжатии строки. Вам необходимо написать программу, которая сжимает заданную строку, заменяя повторяющиеся символы на число повторений и сам символ. */

class Program
{
    static string CompressString(string input)
    {
        StringBuilder compressed = new StringBuilder();
        int count = 1;

        for (int i = 1; i <= input.Length; i++)
        {
            if (i < input.Length && input[i] == input[i - 1])
            {
                count++;
            }
            else
            {
                compressed.Append(count);
                compressed.Append(input[i - 1]);
                count = 1;
            }
        }

        return compressed.ToString();
    }

    static void Main()
    {
        string input = Console.ReadLine();
        string compressedString = CompressString(input);

        Console.WriteLine("Сжатая строка: " + compressedString);
    }
}
