using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using HeronGenerator.Generators;
using HeronGenerator.Models;
using Newtonsoft.Json;

namespace HeronGenerator
{
    class Program
    {
        static void Main(string[] args)
        {
            var exampleText = File.ReadAllText(@"Examples/doctor-salary-indicator.json");
            var indicator = JsonConvert.DeserializeObject<Indicator>(exampleText);
            var result = SpoutGenerator.GenerateSpout(indicator.Indices, indicator.Name);
            Console.WriteLine(result);
            Console.WriteLine("Hello World!");
        }
    }
}
