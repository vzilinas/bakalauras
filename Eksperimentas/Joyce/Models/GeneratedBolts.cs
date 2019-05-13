using System;
using System.Collections.Generic;

namespace Joyce.Models
{
    public class GeneratedBolt
    {
        public Guid Id { get; set; }
        public string Output { get; set; }
        public List<string> Inputs { get; set; }
        public string BoltName { get; set; }
        public string GeneratedBoltText { get; set; }
        public List<GeneratedBolt> NextBolts { get; set; }
    }
}