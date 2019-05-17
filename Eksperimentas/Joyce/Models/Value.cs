using System;
using System.Collections.Generic;

namespace Joyce.Models
{
    public class Value
    {
        public Guid Id { get; set; }
        public string FieldName { get; set; }
        public string Formula { get; set; }
        public List<Value> NextValues { get; set; }
    }
}