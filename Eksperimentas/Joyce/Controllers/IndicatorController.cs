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
            Generator.GenerateTopology(indicator);
            BuildTopology(indicator.Name);
            StartHeron(indicator.Name);
            return Ok();
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
