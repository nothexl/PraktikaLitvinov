using System;
using System.Collections.Generic;

/* Дан взвешенный ориентированный граф с n вершинами и m ребрами. Каждое ребро имеет определенную стоимость перехода.
 * Требуется найти кратчайший путь между двумя заданными вершинами в этом графе. Реализуйте алгоритм нахождения кратчайшего пути,
 * такой как алгоритм Дейкстры или алгоритм Беллмана-Форда. */

class Graph
{
    private int V;
    private List<(int, int)>[] adj;

    public Graph(int vertices)
    {
        V = vertices;
        adj = new List<(int, int)>[V];

        for (int i = 0; i < V; i++)
        {
            adj[i] = new List<(int, int)>();
        }
    }

    public void AddEdge(int u, int v, int weight)
    {
        adj[u].Add((v, weight));
    }

    public int ShortestPath(int source, int destination)
    {
        int[] dist = new int[V];
        bool[] visited = new bool[V];

        for (int i = 0; i < V; i++)
        {
            dist[i] = int.MaxValue;
            visited[i] = false;
        }

        dist[source] = 0;

        for (int count = 0; count < V - 1; count++)
        {
            int u = MinDistance(dist, visited);
            visited[u] = true;

            foreach (var neighbor in adj[u])
            {
                int v = neighbor.Item1;
                int weight = neighbor.Item2;

                if (!visited[v] && dist[u] != int.MaxValue && dist[u] + weight < dist[v])
                {
                    dist[v] = dist[u] + weight;
                }
            }
        }

        return dist[destination];
    }

    private int MinDistance(int[] dist, bool[] visited)
    {
        int min = int.MaxValue;
        int minIndex = -1;

        for (int v = 0; v < V; v++)
        {
            if (!visited[v] && dist[v] <= min)
            {
                min = dist[v];
                minIndex = v;
            }
        }

        return minIndex;
    }
}

class Program
{
    static void Main()
    {
        Graph graph = new Graph(6);
        graph.AddEdge(0, 1, 4);
        graph.AddEdge(0, 2, 1);
        graph.AddEdge(2, 1, 2);
        graph.AddEdge(2, 3, 5);
        graph.AddEdge(3, 4, 3);
        graph.AddEdge(4, 1, 1);
        graph.AddEdge(4, 5, 2);

        int source = 0;
        int destination = 5;

        int shortestPath = graph.ShortestPath(source, destination);

        Console.WriteLine("Кратчайший путь от вершины " + source + " к вершине " + destination + ": " + shortestPath);
    }
}
