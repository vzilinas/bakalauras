using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Joyce.Models;

namespace Joyce.Generators
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
            var primaryKey = new StringBuilder("str(input_dict['");
            primaryKey.AppendJoin("']) + '_' + str(input_dict['", indicator.PrimaryKey);
            primaryKey.Append("'])");

            var primaryKeyArray = new StringBuilder("input_dict['");
            primaryKeyArray.AppendJoin("'], input_dict['", indicator.PrimaryKey);
            primaryKeyArray.Append("']");

            var spoutFile = new StringBuilder(File.ReadAllText(_spoutFileName));

            spoutFile.Replace("<%KafkaQueue%>", _queueName);
            spoutFile.Replace("<%IndicatorId%>", indicator.IndicatorId.ToString());
            spoutFile.Replace("<%IndicatorName%>", indicator.Name);
            spoutFile.Replace("<%IndicatorVersion%>", indicator.VersionId);
            spoutFile.Replace("<%SpoutFilteredDict%>", filteredDict.ToString());

            spoutFile.Replace("<%PrimaryKey%>", primaryKey.ToString());
            spoutFile.Replace("<%PrimaryKeyArray%>", primaryKeyArray.ToString());

            return spoutFile.ToString();

        }
    }
}