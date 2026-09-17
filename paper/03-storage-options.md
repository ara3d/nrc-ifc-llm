# 3. Storage options and recommendation

This section answers the first objective: where should analytics live so that they are
portable, reusable, and queryable at component, zone, storey, and building level. It condenses
the longer options brief in [storing-analytics-in-ifc.md](../storing-analytics-in-ifc.md).

## 3.1 What "storing analytics in IFC" has to achieve

An analytics value is more than a number. To be reusable it needs, at minimum:

- the element or spatial container it describes (`GlobalId`);
- the metric (embodied carbon, energy use intensity);
- the unit;
- the lifecycle stage or time basis (A1 to A3, A1 to A5, annual);
- the scenario (baseline, retrofit option 2);
- the run that produced it, with the tool, method, and date.

Any storage option is judged on how much of this it can carry, and on four properties:
**portability** (does the value travel with the file), **queryability** (can a tool or an LLM
find it without special knowledge), **interoperability** (do other IFC tools read it), and
**scalability** (does it still work for thousands of metrics, many scenarios, or time series).

## 3.2 The twelve options

The options brief examines twelve mechanisms. They are summarised here; the brief gives the
IFC entity references and a fuller discussion of each.

| # | Option | Mechanism | Best for |
|---|---|---|---|
| 1 | Custom property sets | `IfcPropertySet` on elements and containers | Summary values for display and query |
| 2 | Standard environmental Psets | `Pset_EnvironmentalImpactIndicators` and related | Standards-aligned LCA fields |
| 3 | Element quantities | `IfcElementQuantity` | Takeoff inputs (areas, volumes) |
| 4 | Material properties | `IfcMaterialProperties` | Carbon factors, EPD data per material |
| 5 | Spatial aggregates | Property sets on space, storey, building | Dashboards and roll-ups |
| 6 | External dataset reference | `IfcDocumentReference` plus join key | Full analytics tables, time series |
| 7 | Library references | `IfcLibraryInformation` | Reusable metric definitions |
| 8 | Classification references | `IfcClassificationReference`, bsDD | Semantic tagging of metrics |
| 9 | Performance history | `IfcPerformanceHistory` | Operational, time-based performance |
| 10 | Constraints and metrics | `IfcMetric`, `IfcObjective`, `IfcConstraint` | Targets and pass/fail |
| 11 | Visualisation metadata | Colour and legend properties | Presentation hints |
| 12 | Custom schema extension | New entity types | Research; not portable |

Two of the twelve stand out. Option 1 is the simplest and the most widely readable: almost every
IFC viewer shows property sets, and "colour every element by property X" is a standard viewer
feature. Option 6 is the only one that scales: an external Parquet or DuckDB table holds
millions of rows without bloating the IFC, and the IFC keeps a pointer and a join key. The
others are refinements that add meaning (7, 8, 10), cover a special case (3, 4, 9), or should
be avoided for a portability-first project (12).

## 3.3 Comparison matrix

| Option | Portability | Queryability | Interoperability | Scalability |
|---|---|---|---|---|
| Custom property sets | High | High | Medium to high | Medium |
| Standard environmental Psets | High | High | Medium | Medium |
| Element quantities | High | High | High | Medium |
| Material properties | High | Medium | Medium | High |
| Spatial aggregates | High | High | Medium | High |
| External dataset reference | Medium | Very high | Medium | Very high |
| Library and classification references | Medium | Medium | Medium to high | High |
| `IfcPerformanceHistory` | Medium | Medium | Low to medium | Medium |
| Constraints, objectives, metrics | Medium | Medium | Low to medium | Medium |
| Custom schema extension | Low | High with custom tools | Low | Medium |

Portability is scored on whether the value is inside the `.ifc` file. Queryability is scored on
whether a generic IFC parser, or an LLM with generic tools, can find it by name. Interoperability
is scored on how many existing viewers and checkers understand the mechanism.

## 3.4 The three-layer recommendation

No single option satisfies all four properties. The recommendation is to use three together,
each doing the job it is best at.

**Layer 1: summary values in custom property sets.** Write the scalar values that people look
at, filter by, colour by, and ask about, directly into property sets on elements and on spatial
containers. Use one set per topic so that a viewer's property panel stays readable and an IDS can
require the topic as a unit:

```text
Pset_NRCEmbodiedCarbon
Pset_NRCOperationalCarbon
Pset_NRCEnergyPerformance
Pset_NRCAnalyticsProvenance
```

Every set carries `ScenarioName` and `AnalysisRunId` so that a value can never be separated from
the run that produced it. Units and lifecycle stages are in the property names
(`EmbodiedCarbon_A1A3_kgCO2e`) so that they survive tools that drop the IFC unit assignment.
Appendix A gives the full definitions.

**Layer 2: a reference to the full dataset.** Attach an `IfcDocumentReference` to the project
(or to the building) that names the external result table, its format, its checksum, and the
join key. The external table is long-format, one row per (run, element, metric), so that new
metrics never require a schema change:

```text
AnalysisRunId, GlobalId, IfcClass, MetricId, MetricName, Value, Unit,
LifecycleStage, Scenario, Source, Confidence, ComputationMethod
```

Parquet is the recommended format: it is columnar, compressed, typed, and loads into DuckDB,
pandas, and every lakehouse tool. CSV is acceptable for small datasets and for human
inspection.

**Layer 3: a metric dictionary.** Define a short list of metric identifiers and map each property
name in Layer 1 and each `MetricId` in Layer 2 to one of them:

```text
NRC.EC.A1A3.TOTAL      Embodied carbon, stages A1 to A3, kgCO2e
NRC.EC.A1A5.TOTAL      Embodied carbon, stages A1 to A5, kgCO2e
NRC.OC.ANNUAL          Operational carbon, kgCO2e per year
NRC.EUI.ANNUAL         Energy use intensity, kWh per m2 per year
NRC.GWP.MATERIAL_FACTOR Global warming potential factor per material unit
```

The dictionary can be published as an IFC library reference, as a bsDD domain, or simply as a
versioned JSON file shipped with the IDS. Its purpose is to give the query layer (Section 5)
one place to resolve "carbon" to a column, and to give an IDS one vocabulary to require.

## 3.5 Writing property sets without disturbing the file

Layer 1 requires writing into a client's IFC file. Section 2.1 noted that most libraries
re-serialise the whole file. The toolkit's editing library instead treats the source file as
bytes, finds the highest entity id and the owner-history entity, and appends new entities. For
one element and one property set it emits N `IFCPROPERTYSINGLEVALUE` lines, one
`IFCPROPERTYSET`, and one `IFCRELDEFINESBYPROPERTIES`. The `GlobalId` of each new entity is a
deterministic hash of a caller-supplied key, so running the writer twice produces the same
bytes.

```csharp
var original = IfcSourceFile.Load(sourcePath);
var builder = new IfcPropertySetBuilder(
    original.MaxId + 1,
    original.FirstIdOfType("IFCOWNERHISTORY"));

builder.AddPropertySet(wall.Id, "Pset_NRCEmbodiedCarbon",
    new[]
    {
        IfcPropertyValue.Real("EmbodiedCarbon_A1A3_kgCO2e", 412.7),
        IfcPropertyValue.Label("ScenarioName", "Baseline"),
        IfcPropertyValue.Label("AnalysisRunId", "run-2026-07-14-01"),
    },
    guidKey: $"analytics:{wall.GlobalId}:Pset_NRCEmbodiedCarbon");

File.WriteAllBytes(targetPath, IfcPatcher.Append(original, builder.Lines));
```

An entity-level diff (`IfcDiff.Compare`) then reports exactly which entities were added, and
`IfcPatcher.Remove` takes them out again. Section 6.3 shows this round trip verified byte for
byte on the Duplex model. The same path is exposed as the `sink.writePsets` node in the dataflow
graph, where it runs only inside an explicit run.

The practical consequence for NRC is that an enriched file can be given back to a model author
with a diff that lists the additions and nothing else, and the author can strip the additions
and recover their original file exactly.

## 3.6 Recommendation in brief

1. Write summary analytics into custom property sets on elements, spaces, storeys, buildings,
   and the project, using the definitions in Appendix A.
2. Put units, lifecycle stage, scenario, run id, and provenance in every set.
3. Reference the full result table from the IFC with an `IfcDocumentReference`, joined on
   `GlobalId`, stored as Parquet.
4. Publish a small metric dictionary and map every property and metric id to it.
5. Write with a byte-exact patch, never a re-serialisation, so that additions are auditable and
   reversible.
6. Express items 1 to 4 as an IDS specification so that delivered models can be validated.

Items 1, 3, and 5 are implemented and tested in the toolkit. Item 4 is a document. Item 6 is
future work (Section 8).
