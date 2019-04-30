using System;
using System.Collections.Generic;

public class Indicator
{
    public string Name { get; set; }
    public long VersionId { get; set; }
    public DateTimeOffset ActiveFrom { get; set; }
    public DateTimeOffset ActiveTo { get; set; }
    List<Indice> Indices { get; set; }
}