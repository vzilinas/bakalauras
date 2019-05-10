using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
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

            var spout = SpoutGenerator.GenerateSpout(indicator);

            Console.WriteLine(spout);

            var bolts = BoltGenerator.GenerateBolts(indicator);

            //Console.WriteLine(JsonConvert.SerializeObject(bolts));
            var result = bolts.Select(x => Print(x)).ToList();
            result.ForEach(x=> Console.WriteLine(x));
            Console.WriteLine();
        }
        public static string Print(GeneratedBolt bolt)
        {
            var printable = new StringBuilder($"========{bolt.BoltName}========\n");
            printable.Append(bolt.GeneratedBoltText);

            if (bolt.NextBolts == null || bolt.NextBolts.Count == 0)
            {
                return(printable.ToString());
            }
            else
            {
                foreach (var child in bolt.NextBolts)
                {
                    printable.Append(Print(child));
                }
                return printable.ToString();
            }
        }
    }
}
