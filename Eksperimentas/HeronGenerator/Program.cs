using System;
using HeronGenerator.Generators;
using HeronGenerator.Models;

namespace HeronGenerator
{
    class Program
    {
        static void Main(string[] args)
        {
            SpoutGenerator.GenerateSpout(new Indice());
            Console.WriteLine("Hello World!");
        }
    }
}
