namespace Joyce.Models
{
    public class Filter
    {
        public string FieldName { get; set; }
        public Operator Operator { get; set; }
        public string Value { get; set; }
        public ValueType Type { get; set; }
    }
}