using System;
using System.Collections.Generic;

/* Задача о размещении базовых станций (Facility Location Problem) - это задача оптимизации, 
 * которая заключается в выборе оптимального местоположения для размещения базовых станций таким образом, 
 * чтобы обслужить все клиентские местоположения с минимальной стоимостью. */

class Program
{
    class Location
    {
        public double X { get; set; }
        public double Y { get; set; }
    }

    class Facility
    {
        public double X { get; set; }
        public double Y { get; set; }
        public List<Location> Clients { get; set; }

        public Facility(double x, double y)
        {
            X = x;
            Y = y;
            Clients = new List<Location>();
        }

        public double GetCost()
        {
            double totalDistance = 0;
            foreach (var client in Clients)
            {
                double distance = Math.Sqrt(Math.Pow(client.X - X, 2) + Math.Pow(client.Y - Y, 2));
                totalDistance += distance;
            }
            return totalDistance;
        }
    }

    static List<Facility> FindOptimalFacilities(List<Location> clients, List<Location> potentialFacilities, int numFacilities)
    {
        List<Facility> facilities = new List<Facility>();
        for (int i = 0; i < numFacilities; i++)
        {
            facilities.Add(new Facility(potentialFacilities[i].X, potentialFacilities[i].Y));
        }

        foreach (var client in clients)
        {
            double minDistance = double.MaxValue;
            Facility closestFacility = null;

            foreach (var facility in facilities)
            {
                double distance = Math.Sqrt(Math.Pow(client.X - facility.X, 2) + Math.Pow(client.Y - facility.Y, 2));
                if (distance < minDistance)
                {
                    minDistance = distance;
                    closestFacility = facility;
                }
            }

            closestFacility.Clients.Add(client);
        }

        return facilities;
    }

    static void Main()
    {
        List<Location> clients = new List<Location>
        {
            new Location { X = 1, Y = 2 },
            new Location { X = 3, Y = 4 },
            new Location { X = 5, Y = 6 },
            new Location { X = 7, Y = 8 }
        };

        List<Location> potentialFacilities = new List<Location>
        {
            new Location { X = 0, Y = 0 },
            new Location { X = 2, Y = 2 },
            new Location { X = 4, Y = 4 },
            new Location { X = 6, Y = 6 },
            new Location { X = 8, Y = 8 }
        };

        int numFacilities = 2;

        List<Facility> optimalFacilities = FindOptimalFacilities(clients, potentialFacilities, numFacilities);

        Console.WriteLine("Оптимальные объекты:");
        foreach (var facility in optimalFacilities)
        {
            Console.WriteLine("Объект в ({0}, {1}) обслуживает {2} клиентов", facility.X, facility.Y, facility.Clients.Count);
        }

        double totalCost = 0;
        foreach (var facility in optimalFacilities)
        {
            totalCost += facility.GetCost();
        }

        Console.WriteLine("Итоговая стоимость: " + totalCost);
    }
}
