using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Joyce.Generators;
using Joyce.Models;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;

namespace Joyce.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class IndicatorController : ControllerBase
    {
        // POST api/values
        [HttpPost]
        public IActionResult Post([FromBody]Indicator indicator)
        {
            StopHeron(indicator.Name);
            MakeDirectory(indicator.Name);
            GenerateTopology(indicator);
            BuildTopology(indicator.Name);
            StartHeron(indicator.Name);
            return Ok();
        }
        private void GenerateTopology(Indicator indicator)
        {
            var spout = SpoutGenerator.GenerateSpout(indicator);

            var bolts = BoltGenerator.GenerateBolts(indicator);

            var emitterBolt = BoltGenerator.GenerateEmitterBolt(indicator);

            var topology = TopologyGenerator.GenerateTopology(indicator.Name, bolts, emitterBolt);
            
            var buildFile = BuildFileGenerator.GenerateBuildFile(indicator.Name);
            
            
            System.IO.File.WriteAllText($"Generated/src/python/{indicator.Name}/BUILD", buildFile);

            System.IO.File.WriteAllText($"Generated/src/python/{indicator.Name}/kafka_input_spout.py", spout);
            bolts.ForEach(x => SaveToFile(x, indicator.Name));
            System.IO.File.WriteAllText($"Generated/src/python/{indicator.Name}/emitter_bolt.py", emitterBolt.GeneratedBoltText);
            System.IO.File.WriteAllText($"Generated/src/python/{indicator.Name}/" + indicator.Name + ".py", topology);
            System.IO.File.WriteAllText($"Generated/src/python/{indicator.Name}/helpers.py", System.IO.File.ReadAllText(@"Templates/helpers.py"));

        }
        public static void SaveToFile(GeneratedBolt bolt, string topologyName)
        {
            System.IO.File.WriteAllText($"Generated/src/python/{topologyName}/" + bolt.BoltName + ".py", bolt.GeneratedBoltText);

            if (bolt.NextBolts == null || bolt.NextBolts.Count == 0)
            {
                return;
            }
            else
            {
                foreach (var child in bolt.NextBolts)
                {
                    SaveToFile(child, topologyName);
                }
                return;
            }
        }
        
        private void MakeDirectory(string topologyName)
        {
            var process = new Process()
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "/bin/bash",
                    Arguments = $"-c \"mkdir Generated/src/python/{topologyName}\"", 					 
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                }
            };
            
            process.Start();
            string result = process.StandardOutput.ReadToEnd();
            process.WaitForExit();
        }
        private void StopHeron(string topologyName)
        {
            var process = new Process()
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "/bin/bash",
                    Arguments = $"-c \"heron kill local {topologyName}\"", 					 
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                }
            };
            
            process.Start();
            string result = process.StandardOutput.ReadToEnd();
            process.WaitForExit();
        }
        private void BuildTopology(string topologyName)
        {
            var process = new Process()
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "/bin/bash",
                    Arguments = $"-c \"sudo ./Generated/pants binary src/python/{topologyName}\"", 					 
                    // Arguments = $"-c \"ls -a\"", 					 
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                }
            };
            
            process.Start();
            string result = process.StandardOutput.ReadToEnd();
            process.WaitForExit();
            Console.WriteLine(result);
        }
        private void StartHeron(string topologyName)
        {
            var process = new Process()
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "/bin/bash",
                    Arguments = $"-c \"heron submit local Generated/dist/{topologyName}.pex - {topologyName}\"", 					 
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                }
            };
            
            process.Start();
            string result = process.StandardOutput.ReadToEnd();
            process.WaitForExit();
        }
    }
}
