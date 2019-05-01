using System;
using System.IO;
using HeronGenerator.Models;

namespace HeronGenerator.Generators
{
    public static class TopologyGenerator
    {
        private static readonly string _topologyFileName = "@Templates/topology.py";
        public static string GenerateTopology()
        {
            string text = File.ReadAllText(_topologyFileName);  
            Console.WriteLine(text); 
            return ""; 
        }
    }
}