// Writes property sets from poc/data/psets_to_write.csv into a copy of duplex.ifc using the
// byte-exact writer, verifies the addition with an entity diff, proves the edit is reversible
// byte for byte, and writes a JSON report with hashes and counts.
//
// Usage: dotnet run --project poc/EnrichIfc -- <source.ifc> <psets.csv> <target.ifc> <report.json>

using System.Globalization;
using System.Security.Cryptography;
using System.Text.Json;
using Ara3D.Ifc.Tests;
using Ara3D.Utils;

if (args.Length != 4)
{
    Console.Error.WriteLine("usage: EnrichIfc <source.ifc> <psets.csv> <target.ifc> <report.json>");
    return 2;
}
var (sourcePath, csvPath, targetPath, reportPath) = (args[0], args[1], args[2], args[3]);

var groups = ReadGroups(csvPath);
using var source = IfcSourceFile.Load(new FilePath(sourcePath));
var builder = new IfcPropertySetBuilder(source.MaxId + 1, source.FirstIdOfType("IFCOWNERHISTORY"));
var entities = new HashSet<int>();
var values = 0;
foreach (var g in groups)
{
    if (!source.Contains(g.EntityId))
        throw new InvalidOperationException($"entity #{g.EntityId} not in {sourcePath}");
    builder.AddPropertySet(g.EntityId, g.PsetName, g.Values, $"nrc-analytics:{g.EntityId}:{g.PsetName}");
    entities.Add(g.EntityId);
    values += g.Values.Count;
}

var enriched = IfcPatcher.Append(source, builder.Lines);
Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(targetPath))!);
File.WriteAllBytes(targetPath, enriched);

// Verify: diff lists exactly the new entities; removing them restores the source byte for byte.
using var after = IfcSourceFile.Load(new FilePath(targetPath));
var diff = IfcDiff.Compare(source, after);
var diffExact = diff.Added.SequenceEqual(builder.Ids) && diff.Deleted.Count == 0 && diff.Changed.Count == 0;
var restored = IfcPatcher.Remove(after, diff.Added);
var reversible = restored.AsSpan().SequenceEqual(File.ReadAllBytes(sourcePath));

// Determinism: a second append from scratch yields identical bytes.
var second = IfcPatcher.Append(source, new IfcPropertySetBuilder(source.MaxId + 1, source.FirstIdOfType("IFCOWNERHISTORY"))
    .Also(b => { foreach (var g in groups) b.AddPropertySet(g.EntityId, g.PsetName, g.Values, $"nrc-analytics:{g.EntityId}:{g.PsetName}"); })
    .Lines);
var deterministic = second.AsSpan().SequenceEqual(enriched);

var report = new
{
    source = Path.GetFullPath(sourcePath),
    target = Path.GetFullPath(targetPath),
    sourceEntities = source.Count,
    sourceSha256 = Sha(File.ReadAllBytes(sourcePath)),
    targetEntities = after.Count,
    targetSha256 = Sha(enriched),
    propertySetsWritten = groups.Count,
    propertyValuesWritten = values,
    elementsTouched = entities.Count,
    entitiesAdded = diff.Added.Count,
    firstNewId = builder.Ids.First(),
    lastNewId = builder.Ids.Last(),
    diffListsExactlyTheAdditions = diffExact,
    removalRestoresSourceByteForByte = reversible,
    secondRunIsByteIdentical = deterministic,
};
Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(reportPath))!);
File.WriteAllText(reportPath, JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine(JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented = true }));
return diffExact && reversible && deterministic ? 0 : 1;

static string Sha(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();

static List<PsetGroup> ReadGroups(string path)
{
    var groups = new List<PsetGroup>();
    var byKey = new Dictionary<(int, string), PsetGroup>();
    foreach (var line in File.ReadLines(path).Skip(1))
    {
        var cells = SplitCsv(line);
        var key = (int.Parse(cells[0], CultureInfo.InvariantCulture), cells[1]);
        if (!byKey.TryGetValue(key, out var g))
        {
            g = new PsetGroup(key.Item1, key.Item2, new List<IfcPropertyValue>());
            byKey[key] = g;
            groups.Add(g);
        }
        g.Values.Add(cells[3] switch
        {
            "Real" => IfcPropertyValue.Real(cells[2], double.Parse(cells[4], CultureInfo.InvariantCulture)),
            "Integer" => IfcPropertyValue.Integer(cells[2], long.Parse(cells[4], CultureInfo.InvariantCulture)),
            "Label" => IfcPropertyValue.Label(cells[2], cells[4]),
            "Identifier" => IfcPropertyValue.Identifier(cells[2], cells[4]),
            "Text" => IfcPropertyValue.Text(cells[2], cells[4]),
            _ => throw new InvalidOperationException($"unknown value type '{cells[3]}'"),
        });
    }
    return groups;
}

// Minimal RFC 4180 splitter: handles quoted cells with commas and doubled quotes.
static string[] SplitCsv(string line)
{
    var cells = new List<string>();
    var cur = new System.Text.StringBuilder();
    var quoted = false;
    for (var i = 0; i < line.Length; i++)
    {
        var c = line[i];
        if (quoted)
        {
            if (c == '"' && i + 1 < line.Length && line[i + 1] == '"') { cur.Append('"'); i++; }
            else if (c == '"') quoted = false;
            else cur.Append(c);
        }
        else if (c == '"') quoted = true;
        else if (c == ',') { cells.Add(cur.ToString()); cur.Clear(); }
        else cur.Append(c);
    }
    cells.Add(cur.ToString());
    return cells.ToArray();
}

sealed record PsetGroup(int EntityId, string PsetName, List<IfcPropertyValue> Values);

static class Ext
{
    public static T Also<T>(this T self, Action<T> act) { act(self); return self; }
}
