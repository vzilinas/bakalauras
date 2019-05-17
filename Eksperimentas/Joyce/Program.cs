﻿using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Joyce.Generators;
using Joyce.Models;
using Microsoft.AspNetCore;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace Joyce
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var indicator = JsonConvert.DeserializeObject<Indicator>(File.ReadAllText(@"Examples/doctor-salary-indicator.json"));
            Generator.GenerateTopology(indicator);
            //CreateWebHostBuilder(args).Build().Run();
        }

        public static IWebHostBuilder CreateWebHostBuilder(string[] args) =>
            WebHost.CreateDefaultBuilder(args)
                .UseStartup<Startup>();
    }
}
