namespace HeronGenerator.Models
{
    public class Modifier
    {
        public Operator Operator { get; set; }
        public string FieldName {get;set;}
        public string Value {get;set;}
        public ValueType Type {get;set;}
    }
}