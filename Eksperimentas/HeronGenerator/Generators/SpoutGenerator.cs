
using HeronGenerator.Models;

namespace HeronGenerator.Generators
{
    public static class SpoutGenerator
    {
        private static readonly string _spoutFileName = "@Templates/spout.py";
        public static string GenerateSpout(Indice spoutIndice)
        {
            string text = File.ReadAllText(_spoutFileName);  
            Console.WriteLine(text);  
        }
    }
}