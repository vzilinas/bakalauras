using Joyce.Models;

namespace Joyce.Generators
{
    public static class Generator
    {
        public static void GenerateTopology(Indicator indicator)
        {
            var spout = SpoutGenerator.GenerateSpout(indicator);

            var bolts = BoltGenerator.GenerateBolts(indicator);

            var emitterBolt = BoltGenerator.GenerateEmitterBolt(indicator);

            var topology = TopologyGenerator.GenerateTopology(indicator.Name, bolts, emitterBolt);
            
            var buildFile = BuildFileGenerator.GenerateBuildFile(indicator.Name);
            
            
            System.IO.File.WriteAllText($"Generated/src/python/{indicator.Name}/BUILD", buildFile);

            System.IO.File.WriteAllText($"Generated/src/python/{indicator.Name}/kafka_input_spout.py", spout);
            bolts.ForEach(x => SaveToFile(x, indicator.Name));
            System.IO.File.WriteAllText($"Generated/src/python/{indicator.Name}/emitter_bolt.py", emitterBolt.GeneratedBoltText);
            System.IO.File.WriteAllText($"Generated/src/python/{indicator.Name}/" + indicator.Name + ".py", topology);
            System.IO.File.WriteAllText($"Generated/src/python/{indicator.Name}/helpers.py", System.IO.File.ReadAllText(@"Templates/helpers.py"));

        }
        public static void SaveToFile(GeneratedBolt bolt, string topologyName)
        {
            System.IO.File.WriteAllText($"Generated/src/python/{topologyName}/" + bolt.BoltName + ".py", bolt.GeneratedBoltText);

            if (bolt.NextBolts == null || bolt.NextBolts.Count == 0)
            {
                return;
            }
            else
            {
                foreach (var child in bolt.NextBolts)
                {
                    SaveToFile(child, topologyName);
                }
                return;
            }
        }
    }
}