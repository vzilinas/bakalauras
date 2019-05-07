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
        public static string GenerateSpout(Indicator indicator)
        {
            var filteredDict = new StringBuilder("if ");
            if (indicator.Filters?.Any() == true)
            {
                var firstFilter = indicator.Filters.First();
                filteredDict.Append($"input_dict['{firstFilter.FieldName}'] {Converter.Op(firstFilter.Operator)} '{firstFilter.Value}'");
                foreach (var filter in indicator.Filters.Skip(1))
                {
                    filteredDict.Append($" or input_dict['{filter.FieldName}'] {Converter.Op(firstFilter.Operator)} '{filter.Value}'");
                }
                filteredDict.Append(":");
            }
            else
            {
                filteredDict.Append("True:");
            }
            var text = new StringBuilder(File.ReadAllText(_spoutFileName));

            text.Replace("<%KafkaQueue%>", _queueName);
            text.Replace("<%IndicatorId%>", indicator.IndicatorId.ToString());
            text.Replace("<%IndicatorName%>", indicator.Name);
            text.Replace("<%IndicatorVersion%>", indicator.VersionId);
            text.Replace("<%SpoutFilteredDict%>", filteredDict.ToString());

            return text.ToString();

        }
    }
}