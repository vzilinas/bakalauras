using System;
using System.Collections.Generic;
using System.Linq;
using HeronGenerator.Generators;
using HeronGenerator.Models;

namespace HeronGenerator
{
    class Program
    {
        static void Main(string[] args)
        {
            var result = SpoutGenerator.GenerateSpout(new List<Indice>{
                new Indice
                    {
                        FieldName = "Profesija",
                        Value = "Gydytojas",
                        VersionId = 1651564,
                        Operator = Operator.EQU
                    },
                new Indice
                    {
                        FieldName = "Lytis",
                        Value = "Vyras",
                        VersionId = 1651564,
                        Operator = Operator.EQU
                    },
                new Indice
                    {
                        FieldName = "Sritis",
                        Value = "",
                        VersionId = 1651564,
                        Operator = Operator.CMP
                    }
                }, "doctor-salary"
            );
            Console.WriteLine(result.First());
            Console.WriteLine("Hello World!");
        }
    }
}
