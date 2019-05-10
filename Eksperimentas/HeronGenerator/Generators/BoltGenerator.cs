using System;
using System.Linq;
using System.Collections.Generic;
using System.IO;
using System.Text;
using HeronGenerator.Models;
using System.Text.RegularExpressions;

namespace HeronGenerator.Generators
{
    public static class BoltGenerator
    {
        private static readonly string _boltFileName = @"Templates/bolt.py";
        public static List<GeneratedBolt> GenerateBolts(Indicator indicator)
        {
            var results = new List<GeneratedBolt>();
            foreach (var value in indicator.Values)
            {
                results.Add(GenerateBolt(value));
            }
            return results;
        }
        public static GeneratedBolt GenerateBolt(Value value)
        {
            var text = new StringBuilder(File.ReadAllText(_boltFileName));
            text.Replace("<%BoltName%>", value.FieldName + "_" + value.Id);
            // text.Replace("<%VersionId%>", boltIndice.VersionId);
            text.Replace("<%BoltOutputs%>", value.FieldName + "_" + value.Id);
            if (value.NextValues == null || !value.NextValues.Any())
            {
                text.Replace("<%InputValue%>", $"input_dict['data']['{value.FieldName}']");
                return new GeneratedBolt
                {
                    BoltName = value.FieldName + "_" + value.Id,
                    Id = value.Id,
                    Output = value.FieldName + "_" + value.Id,
                    Inputs = null,
                    NextBolts = null,
                    GeneratedBoltText = text.ToString()
                };
            }
            else
            {
                var combinationDefinition = ParseFormula(value);
                text.Replace("<%InputValue%>", combinationDefinition);
                return new GeneratedBolt
                {
                    BoltName = value.FieldName + "_" + value.Id,
                    Id = value.Id,
                    Output = value.FieldName + "_" + value.Id,
                    Inputs = value.NextValues.Select(x => x.FieldName + "_" + x.Id).ToList(),
                    NextBolts = value.NextValues.Select(x => GenerateBolt(x)).ToList(),
                    GeneratedBoltText = text.ToString()
                };
            }
        }
        public static string ParseFormula(Value value)
        {
            var parsed = new StringBuilder();

            parsed.Append(value.Formula);
            var regex = new Regex(@"%(.+?)%");
            var elements = regex.Matches(value.Formula);
            foreach (var element in elements)
            {
                var definition = value.NextValues.First(x => x.Id == new Guid(element.ToString().Trim('%')));
                parsed.Replace(element.ToString(), $"input_dict['result']['{definition.FieldName + "_" + definition.Id}']['last_value']");
            }
            return parsed.ToString();
        }
    }
}