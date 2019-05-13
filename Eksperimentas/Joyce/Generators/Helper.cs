using System.Text;

namespace Joyce.Generators
{
    public static class Helper
    {
        public static string GetClassName(string boltName)
        {
            var className = new StringBuilder(boltName.Substring(0,25));
            className.Replace("_", string.Empty);
            className.Replace("-", string.Empty);
            return className.ToString();
        }
    }
}