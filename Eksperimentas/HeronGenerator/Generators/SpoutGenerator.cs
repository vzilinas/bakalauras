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
        public static string GenerateSpout(List<Indice> spoutIndices, string indicatorName)
        {
            var filterIndices = spoutIndices.Where(x => x.Operator == Operator.EQU);
            var comparerIndice = spoutIndices.FirstOrDefault(x => x.Operator == Operator.CMP);
            var filteredDict = new StringBuilder("if (");
            foreach (var indice in filterIndices)
            {
                filteredDict.Append($"inputDict['{indice.FieldName}'] == '{indice.Value}' and ");
            }
            filteredDict.Append(")");
            var filtered = filteredDict.ToString();
            var lastAnd = filtered.LastIndexOf(" and ");
            filtered = filtered.Remove(lastAnd, 5);
            var text = new StringBuilder(File.ReadAllText(_spoutFileName));

            text.Replace("<%KafkaQueue%>", _queueName);
            text.Replace("<%VersionId%>", comparerIndice.VersionId);
            text.Replace("<%SpoutOutputs%>", indicatorName);
            text.Replace("<%SpoutFilteredDict%>", filtered);
            text.Replace("<%SpoutComparator%>", comparerIndice.FieldName);

            return text.ToString();
        }
    }
}