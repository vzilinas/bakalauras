using System;
using System.Collections.Generic;

namespace HeronGenerator.Models
{
    public class Indicator
    {
        public Guid IndicatorId { get; set; }
        public string Name { get; set; }
        public string VersionId { get; set; }
        public DateTimeOffset ActiveFrom { get; set; }

        public List<string> PrimaryKey { get; set; }
        public List<Filter> Filters { get; set; }
        public List<Value> Values { get; set; }
    }
}