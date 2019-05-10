using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using HeronGenerator.Models;

namespace HeronGenerator.Generators
{
    public static class TopologyGenerator
    {
        private static readonly string _topologyFileName = @"Templates/topology.py";
        public static string GenerateTopology(string indicatorName, List<GeneratedBolt> bolts, GeneratedBolt emitterBolt)
        {
            var file = File.ReadAllText(_topologyFileName);
            var text = new StringBuilder(file);
            text.Replace("<%TopologyName%>", indicatorName);
            text.Replace("<%EmitterInputs%>", GenerateInputs(emitterBolt));
            text.Replace("<%TopologyBoltImports%>", GenerateTopologyImports(bolts));
            text.Replace("<%TopolgyBoltDefinitions%>", GenerateTopologyDefinitions(bolts));
            return text.ToString(); 
        }
        private static string GenerateInputs(GeneratedBolt emitter)
        {
            var inputs = new StringBuilder();
            inputs.AppendJoin(", ", emitter.Inputs.Select(x=> $"{GetClassName(x).ToLower()}_bolt : Grouping.fields('{x}')"));
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
            var printable = new StringBuilder($"from {bolt.BoltName} import {GetClassName(bolt.BoltName)}\n");
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
        private static string GetClassName(string boltName)
        {
            var className = new StringBuilder(boltName.Substring(0,25));
            className.Replace("_", string.Empty);
            className.Replace("-", string.Empty);
            return className.ToString();
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
            var boltName = GetClassName(bolt.BoltName).ToLower();
            var printable = new StringBuilder(
                $"    {boltName}_bolt = builder.add_bolt('{boltName}', {GetClassName(bolt.BoltName)}, par=2)\n");
            if (bolt.NextBolts == null || bolt.NextBolts.Count == 0)
            {
                printable.Append("\tinputs = {kafka_input_spout : Grouping.fields('SpoutOutput');})\n");
                return(printable.ToString());
            }
            else
            {
                printable.Append("\tinputs = {" + GenerateInputs(bolt) + "})\n");
                foreach (var child in bolt.NextBolts)
                {
                    printable.Append(GenerateDefinition(child));
                }
                return printable.ToString();
            }
        }
    }
}