using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using HeronGenerator.Models;

namespace HeronGenerator.Generators
{
    public static class SpoutGenerator
    {
        private static readonly string _queueName = "statistics-queue";
        private static readonly string _spoutFileName = @"Templates/spout.py";
        public static (string, List<Indice>) GenerateSpout(Indice spoutIndice)
        {

            var filterModifiers = spoutIndice.Modifiers.Where(x => x.Operator == Operator.EQU);
            var filteredDict = new StringBuilder("if (");
            foreach (var filter in filterModifiers)
            {
                filteredDict.Append($"inputDict['{filter.FieldName}'] == '{filter.Value}' or ");
            }
            filteredDict.Append(")");
            var filtered = filteredDict.ToString();
            var lastAnd = filtered.LastIndexOf(" or ");
            filtered = filtered.Remove(lastAnd, 5);
            var text = new StringBuilder(File.ReadAllText(_spoutFileName));

            text.Replace("<%KafkaQueue%>", _queueName);
            text.Replace("<%VersionId%>", spoutIndice.VersionId);
            text.Replace("<%SpoutOutputs%>", spoutIndice.FieldName + spoutIndice.Operator);
            text.Replace("<%SpoutFilteredDict%>", filtered);

            return (text.ToString(), spoutIndice.LowerLevel);

        }
    }
}