using System;
using System.Collections.Generic;

namespace HeronGenerator.Models
{
    public class Indice
    {
        public string FieldName { get; set; }
        public string Value { get; set; }
        public DateTimeOffset ActiveFrom { get; set; }
        public long VersionId { get; set; }
        public Operator Operator { get; set; }
        public List<Indice> LowerLevel { get; set; }
    }
}