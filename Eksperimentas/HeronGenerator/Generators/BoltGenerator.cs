using System;
using System.Collections.Generic;
using System.IO;
using HeronGenerator.Models;

namespace HeronGenerator.Generators
{
    public static class BoltGenerator
    {
        private static readonly string _boltFileName = "@Templates/bolt.py";
        public static string GenerateBolt(List<Indice> boltIndices)
        {
            string text = File.ReadAllText(_boltFileName);  
            Console.WriteLine(text);  
            return "";
        }
    }
}