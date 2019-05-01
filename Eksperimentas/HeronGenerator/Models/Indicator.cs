using System;
using System.Collections.Generic;

namespace HeronGenerator.Models
{
    public class Indicator
    {
        public string Name { get; set; }
        public string VersionId { get; set; }
        public DateTimeOffset ActiveFrom { get; set; }
        public DateTimeOffset? ActiveTo { get; set; }
        public List<Indice> Indices { get; set; }
    }
}