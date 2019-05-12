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
        private static readonly string _emitterBoltFileName = @"Templates/emitter_bolt.py";
        public static GeneratedBolt GenerateEmitterBolt(Indicator indicator)
        {
            var text = new StringBuilder(File.ReadAllText(_emitterBoltFileName));
            text.Replace("<%IndicatorName%>", indicator.Name);
            return new GeneratedBolt
            {
                BoltName = "emitter_bolt",
                GeneratedBoltText = text.ToString(),
                Inputs = indicator.Values.Select( x=> x.FieldName + "_" + x.Id).ToList()
            };
        }
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
            text.Replace("<%BoltName%>", Helper.GetClassName(value.FieldName + "_" + value.Id));
            // text.Replace("<%VersionId%>", boltIndice.VersionId);
            text.Replace("<%BoltOutputs%>", value.FieldName + "_" + value.Id);
            if (value.NextValues == null || !value.NextValues.Any())
            {
                text.Replace("<%Combined%>", "False");
                text.Replace("<%CombinedCheck%>", "'empty'");
                text.Replace("<%InputValue%>", $"input_dict['data']['{value.FieldName}']");
                return new GeneratedBolt
                {
                    BoltName = Helper.GetClassName(value.FieldName + "_" + value.Id),
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
                text.Replace("<%Combined%>", "True");
                var combinedCheck = value.NextValues.Select(x => $"'{Helper.GetClassName(x.FieldName + "_" + x.Id)}'");
                text.Replace("<%CombinedCheck%>", string.Join(", ", combinedCheck));
                text.Replace("<%InputValue%>", combinationDefinition);
                return new GeneratedBolt
                {
                    BoltName = Helper.GetClassName(value.FieldName + "_" + value.Id),
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
                parsed.Replace(element.ToString(), $"self.temp_combination[output_dict['unique_id']]['{Helper.GetClassName(definition.FieldName + "_" + definition.Id)}']['last_value']");
            }
            return parsed.ToString();
        }
    }
}