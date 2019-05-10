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

            var bolts = BoltGenerator.GenerateBolts(indicator);

            var emitterBolt = BoltGenerator.GenerateEmitterBolt(indicator);

            var topology = TopologyGenerator.GenerateTopology(indicator.Name, bolts, emitterBolt);
            
            File.WriteAllText(@"Generated/kafka_input_spout.py", spout);
            bolts.ForEach(x=> SaveToFile(x));
            File.WriteAllText(@"Generated/emitter_bolt.py", emitterBolt.GeneratedBoltText);
            File.WriteAllText(@"Generated/" + indicator.Name + ".py", topology);

            Console.WriteLine();
        }
        public static void SaveToFile(GeneratedBolt bolt)
        {
            File.WriteAllText(@"Generated/" + bolt.BoltName + ".py", bolt.GeneratedBoltText);

            if (bolt.NextBolts == null || bolt.NextBolts.Count == 0)
            {
                return;
            }
            else
            {
                foreach (var child in bolt.NextBolts)
                {
                    SaveToFile(child);
                }
                return;
            }
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
