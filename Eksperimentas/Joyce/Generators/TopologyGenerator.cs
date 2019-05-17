using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Joyce.Models;

namespace Joyce.Generators
{
    public static class TopologyGenerator
    {
        private static readonly string _topologyFileName = @"Templates/topology.py";
        public static string GenerateTopology(string indicatorName, List<GeneratedBolt> bolts, GeneratedBolt emitterBolt)
        {
            var file = File.ReadAllText(_topologyFileName);
            var text = new StringBuilder(file);
            text.Replace("<%TopologyName%>", indicatorName);
            text.Replace("<%EmitterInputs%>", string.Join(", ", bolts.Select(x=>GenerateEmitterInput(x))));
            text.Replace("<%TopologyBoltImports%>", GenerateTopologyImports(bolts));
            text.Replace("<%TopolgyBoltDefinitions%>", GenerateTopologyDefinitions(bolts));
            return text.ToString(); 
        }
        private static string GenerateEmitterInput(GeneratedBolt bolt)
        {
            var printable = new StringBuilder($"{bolt.BoltName.ToLower()}_bolt : Grouping.SHUFFLE");
            if (bolt.NextBolts == null || bolt.NextBolts.Count == 0)
            {
                return(printable.ToString());
            }
            else
            {
                foreach (var child in bolt.NextBolts)
                {
                    printable.Append(", " + GenerateEmitterInput(child));
                }
                return printable.ToString();
            }
        }

        private static string GenerateInputs(GeneratedBolt emitter)
        {
            var inputs = new StringBuilder();
            inputs.AppendJoin(", ", emitter.Inputs.Select(x=> $"{Helper.GetClassName(x).ToLower()}_bolt : Grouping.fields('unique_id')"));
            return inputs.ToString();
        }
        private static string GenerateTopologyImports(List<GeneratedBolt> bolts)
        {
            var inputs = new StringBuilder();
            var imports = bolts.Select(x=> GenerateImport(x));
            inputs.AppendJoin("", imports);
            return inputs.ToString();
        }
        private static string GenerateImport(GeneratedBolt bolt)
        {
            var printable = new StringBuilder($"from {bolt.BoltName} import {bolt.BoltName}\n");
            if (bolt.NextBolts == null || bolt.NextBolts.Count == 0)
            {
                return(printable.ToString());
            }
            else
            {
                foreach (var child in bolt.NextBolts)
                {
                    printable.Append(GenerateImport(child));
                }
                return printable.ToString();
            }
        }

        private static string GenerateTopologyDefinitions(List<GeneratedBolt> bolts)
        {
            var inputs = new StringBuilder();
            var definitions = bolts.Select(x=> GenerateDefinition(x));
            inputs.AppendJoin("", definitions);
            return inputs.ToString();
        }
        private static string GenerateDefinition(GeneratedBolt bolt)
        {
            var printable = new StringBuilder();
            var boltName = bolt.BoltName.ToLower();
            if (bolt.NextBolts == null || bolt.NextBolts.Count == 0)
            {
                printable.Append($"    {boltName}_bolt = builder.add_bolt('{boltName}', {bolt.BoltName}, par=1, ");
                printable.Append("inputs = {kafka_input_spout : Grouping.SHUFFLE})\n");
                return(printable.ToString());
            }
            else
            {
                foreach (var child in bolt.NextBolts)
                {
                    printable.Append(GenerateDefinition(child));
                }
                printable.Append($"    {boltName}_bolt = builder.add_bolt('{boltName}', {bolt.BoltName}, par=1, ");
                printable.Append("inputs = {" + GenerateInputs(bolt) + "})\n");

                return printable.ToString();
            }
        }
    }
}