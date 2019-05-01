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
            foreach(var spoutIndice in indicator.Indices)
            {
                var (spout, boltIndices) = SpoutGenerator.GenerateSpout(spoutIndice);
                Console.WriteLine(spout);
                foreach(var boltIndice in boltIndices)
                {
                    var bolts = BoltGenerator.GenerateBolts(boltIndice, new List<string>(), new List<string>());
                    bolts.Item2.ForEach(x=>Console.WriteLine(x));                
                }   
            }
            Console.WriteLine("Hello World!");
        }
    }
}
