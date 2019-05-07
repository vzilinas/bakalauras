namespace HeronGenerator.Models
{
    public enum Operator
    {
        EQU,
        NEQU,
        MORE,
        LESS

    }
    static class Converter
    {
        public static string Op(this Operator op)
        {
            switch (op)
            {
                case Operator.EQU:
                    return "==";
                case Operator.NEQU:
                    return "!=";        
                case Operator.MORE:                   
                    return ">";            
                case Operator.LESS:
                    return "<";
                default:
                    return "?!";
            }
        }
    }
}