using System;
using System.Linq;
using System.Collections.Generic;
using System.IO;
using System.Text;
using Joyce.Models;
using System.Text.RegularExpressions;
using StackExchange.Redis;
using MsgPack.Serialization;

namespace Joyce.Generators
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
                Inputs = indicator.Values.Select(x => x.FieldName + "_" + x.Id).ToList()
            };
        }
        public static List<GeneratedBolt> GenerateBolts(Indicator indicator)
        {
            var redisConnection = ConnectionMultiplexer.Connect("localhost");
            var serializer = MessagePackSerializer.Get<BoltKeyState>();
            var results = new List<GeneratedBolt>();
            foreach (var value in indicator.Values)
            {
                results.Add(GenerateBolt(value, indicator.Name, redisConnection, serializer));
            }
            return results;
        }
        public static GeneratedBolt GenerateBolt(Value value, 
                                                string indicatorName, 
                                                ConnectionMultiplexer redisConnection, 
                                                MessagePackSerializer<BoltKeyState> serializer)
        {
            var text = new StringBuilder(File.ReadAllText(_boltFileName));
            text.Replace("<%BoltName%>", Helper.GetClassName(value.FieldName + "_" + value.Id));
            text.Replace("<%PreviousResults%>", GeneratePreviousInputs(indicatorName, 
                                                                        Helper.GetClassName(value.FieldName + "_" + value.Id), 
                                                                        redisConnection, 
                                                                        serializer));
            text.Replace("<%BoltOutputs%>", value.FieldName + "_" + value.Id);
            text.Replace("<%IndicatorName%>", indicatorName);
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
                    NextBolts = value.NextValues.Select(x => GenerateBolt(x, indicatorName, redisConnection, serializer)).ToList(),
                    GeneratedBoltText = text.ToString()
                };
            }
        }
        private static string ParseFormula(Value value)
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

        private static string GeneratePreviousInputs(string indicatorName, 
                                                    string boltName, 
                                                    ConnectionMultiplexer connection, 
                                                    MessagePackSerializer<BoltKeyState> serializer)
        {
            var v = indicatorName + ":" + boltName + ":";
            var redis = connection.GetDatabase();
            var data = redis.SetMembers(v + "state_values");
            if(!data.Any())
            {                
                redis.SetAdd(indicatorName + ":spout_names", boltName);
                return "";
            }
            var previousState = new StringBuilder();
            foreach(var resultName in data)
            {
                var singleResult = serializer.UnpackSingleObject(redis.StringGet(v + resultName.ToString()));
                previousState.Append($"\t\t\t'{resultName.ToString()}' : " + "{\n");
                previousState.Append($"\t\t\t    'Count' : {singleResult.Count},\n");
                previousState.Append($"\t\t\t    'Sum' : {singleResult.Sum},\n");
                previousState.Append("\t\t\t},\n");
            }
            return previousState.ToString();
        }
    }
}