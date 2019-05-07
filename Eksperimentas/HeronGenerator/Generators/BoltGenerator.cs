// using System;
// using System.Linq;
// using System.Collections.Generic;
// using System.IO;
// using System.Text;
// using HeronGenerator.Models;

// namespace HeronGenerator.Generators
// {
//     public static class BoltGenerator
//     {
//         private static readonly string _boltFileName = @"Templates/bolt.py";
//         public static (Indice, List<string>, List<string>) GenerateBolts(Indice boltIndice, List<string> bolts, List<string> boltNames)
//         {
//             bolts.Add(GenerateBolt(boltIndice));
//             boltNames.Add(boltIndice.FieldName + boltIndice.Operator);

//             if (boltIndice.LowerLevel == null || !boltIndice.LowerLevel.Any())
//             {
//                 return (null, bolts, boltNames);
//             }
//             else
//             {
//                 var result = (boltIndice, bolts, boltNames);
//                 foreach (var indice in boltIndice.LowerLevel)
//                 {
//                     result = GenerateBolts(indice, bolts, boltNames);
//                 }
//                 return result;
//             }
//         }
//         public static string GenerateBolt(Indice boltIndice)
//         {
//             var text = new StringBuilder(File.ReadAllText(_boltFileName));
//             text.Replace("<%BoltName%>", boltIndice.FieldName + boltIndice.VersionId);
//             text.Replace("<%VersionId%>", boltIndice.VersionId);
//             text.Replace("<%BoltOutputs%>", boltIndice.FieldName + boltIndice.VersionId);
//             var boltFunction = new StringBuilder();
//             if (boltIndice.Modifiers != null && boltIndice.Modifiers.Any())
//             {
//                 var filterModifiers = boltIndice.Modifiers.Where(x => x.Operator == Operator.EQU);
//                 var dataModifiers = boltIndice.Modifiers.Where(x => x.Operator != Operator.EQU);
//                 if (filterModifiers.Any())
//                 {
//                     boltFunction.Append("if ");
//                     boltFunction.Append($"data['{filterModifiers.First().FieldName}'] == '{filterModifiers.First().Value}'");
//                     foreach (var filter in filterModifiers.Skip(1))
//                     {
//                         boltFunction.Append($" or data['{filter.FieldName}'] == '{filter.Value}'");
//                     }
//                     boltFunction.Append(":\n");
//                     if (dataModifiers.Any())
//                     {
//                         foreach (var dataMod in dataModifiers)
//                         {
//                             boltFunction.Append("\t    ");
//                             switch (dataMod.Operator)
//                             {
//                                 case Operator.SUM:
//                                     boltFunction.Append($"data['{dataMod.FieldName}'] = data['{dataMod.FieldName}'] + {dataMod.Value}");
//                                     break;
//                                 case Operator.SUB:
//                                     boltFunction.Append($"data['{dataMod.FieldName}'] = data['{dataMod.FieldName}'] - {dataMod.Value}");
//                                     break;
//                                 case Operator.MUL:
//                                     boltFunction.Append($"data['{dataMod.FieldName}'] = data['{dataMod.FieldName}'] * {dataMod.Value}");
//                                     break;
//                                 case Operator.DIV:
//                                     boltFunction.Append($"data['{dataMod.FieldName}'] = data['{dataMod.FieldName}'] / {dataMod.Value}");
//                                     break;
//                                 case Operator.MOD:
//                                     boltFunction.Append($"data['{dataMod.FieldName}'] = data['{dataMod.FieldName}'] % {dataMod.Value}");
//                                     break;
//                             }
//                             boltFunction.Append("\n");
//                         }
//                         boltFunction.Append("\t    self.emit[data]\n\t}\n");
//                     }
//                     else
//                     {
//                         boltFunction.Append("\t    self.emit[data]\n\t}\n");
//                     }
//                 }
//                 else
//                 {
//                     if (dataModifiers.Any())
//                     {
//                         foreach (var dataMod in dataModifiers)
//                         {
//                             switch (dataMod.Operator)
//                             {
//                                 case Operator.SUM:
//                                     boltFunction.Append($"data = data + {dataMod.Value}");
//                                     break;
//                                 case Operator.SUB:
//                                     boltFunction.Append($"data = data - {dataMod.Value}");
//                                     break;
//                                 case Operator.MUL:
//                                     boltFunction.Append($"data = data * {dataMod.Value}");
//                                     break;
//                                 case Operator.DIV:
//                                     boltFunction.Append($"data = data / {dataMod.Value}");
//                                     break;
//                                 case Operator.MOD:
//                                     boltFunction.Append($"data = data % {dataMod.Value}");
//                                     break;
//                             }
//                             boltFunction.Append("\n");
//                             boltFunction.Append("\t");
//                         }
//                         boltFunction.Append("self.emit[data]\n");
//                     }
//                 }
//             }
//             else
//             {
//                 boltFunction.Append("self.emit[data]\n");
//             }
//             text.Replace("<%BoltFunction%>", boltFunction.ToString());
//             return text.ToString();
//         }
//     }
// }