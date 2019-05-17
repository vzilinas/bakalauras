using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Joyce.Generators;
using Joyce.Models;
using Microsoft.AspNetCore.Mvc;
using MsgPack.Serialization;
using Newtonsoft.Json;
using StackExchange.Redis;

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
        [HttpGet("{indicatorName}")]
        public IActionResult Get(string indicatorName)
        {
            Console.WriteLine(indicatorName);
            var result = new Dictionary<string, List<Result>>();
            var redisConnection = ConnectionMultiplexer.Connect("localhost");
            var serializer = MessagePackSerializer.Get<BoltKeyState>();
            var redis = redisConnection.GetDatabase();
            var bolts = redis.SetMembers($"{indicatorName}:bolt_names");      
            foreach(var bolt in bolts)
            {
                var values = redis.SetMembers($"{indicatorName}:{bolt}:state_values");
                var tempList = new List<Result>();
                foreach(var value in values)
                {
                    Console.WriteLine(bolt);
                    var temp = serializer.UnpackSingleObject(redis.StringGet($"{indicatorName}:{bolt}:{value}"));
                    tempList.Add(new Result {
                        PrimaryKey = value.ToString(),
                        Count = temp.Count,
                        Sum = temp.Sum                        
                    });
                }
                result.Add(bolt, tempList);
            }
            return Ok(result);
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
