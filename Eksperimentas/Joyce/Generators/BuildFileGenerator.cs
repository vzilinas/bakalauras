using System;
using System.Linq;
using System.Collections.Generic;
using System.IO;
using System.Text;
using Joyce.Models;
using System.Text.RegularExpressions;

namespace Joyce.Generators
{
    public static class BuildFileGenerator
    {
        private static readonly string _buildFileName = @"Templates/BUILD_template";
        public static string GenerateBuildFile(string indicatorName)
        {
            var text = new StringBuilder(File.ReadAllText(_buildFileName));
            text.Replace("<%TopologyName%>", indicatorName);
            return text.ToString();
        }
    }
}