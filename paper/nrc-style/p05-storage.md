# 5 Storage of analytics within IFC

This section addresses the first objective of the statement of work, namely where analytics should reside so that they are portable, reusable, and queryable at component, zone, storey, and building level. It condenses the longer options brief [21].

## 5.1 Requirements on a storage mechanism

An analytics value is more than a number. To be reusable it requires, at minimum, the element or spatial container it describes, identified by `GlobalId`; the metric, such as embodied carbon or energy use intensity; the unit; the lifecycle stage or time basis, such as A1 to A3, A1 to A5, or annual; the scenario, such as baseline or retrofit option 2; and the run that produced it, with the tool, method, and date.

Each candidate mechanism is judged on how much of this it is able to carry, and on four properties. Portability is whether the value travels with the file. Queryability is whether a tool or a language model is able to find it without special knowledge. Interoperability is whether other IFC tools read it. Scalability is whether the mechanism still works for thousands of metrics, many scenarios, or time series.

## 5.2 The twelve mechanisms

The options brief [21] examines twelve mechanisms, which are summarised in Table 3; the brief gives the IFC entity references and a fuller discussion of each.

**Table 3** Twelve mechanisms available within IFC 4.3 for carrying analytics.

| # | Mechanism | IFC basis | Best suited to |
|---|---|---|---|
| 1 | Custom property sets | `IfcPropertySet` on elements and containers | Summary values for display and query |
| 2 | Standard environmental property sets | `Pset_EnvironmentalImpactIndicators` and related | Standards-aligned LCA fields |
| 3 | Element quantities | `IfcElementQuantity` | Takeoff inputs such as areas and volumes |
| 4 | Material properties | `IfcMaterialProperties` | Carbon factors and EPD data per material |
| 5 | Spatial aggregates | Property sets on space, storey, building | Dashboards and roll-ups |
| 6 | External dataset reference | `IfcDocumentReference` with a join key | Full analytics tables and time series |
| 7 | Library references | `IfcLibraryInformation` | Reusable metric definitions |
| 8 | Classification references | `IfcClassificationReference`, bsDD | Semantic tagging of metrics |
| 9 | Performance history | `IfcPerformanceHistory` | Operational, time-based performance |
| 10 | Constraints and metrics | `IfcMetric`, `IfcObjective`, `IfcConstraint` | Targets and pass or fail |
| 11 | Visualisation metadata | Colour and legend properties | Presentation hints |
| 12 | Custom schema extension | New entity types | Research; not portable |

Two of the twelve are distinguished from the rest. Mechanism 1 is the simplest and the most widely readable, in that almost every IFC viewer displays property sets and "colour every element by property X" is a standard viewer feature. Mechanism 6 is the only one that scales, in that an external Parquet or DuckDB table holds millions of rows without inflating the IFC file while the IFC retains a pointer and a join key. The remainder are refinements that add meaning (7, 8, 10), cover a special case (3, 4, 9), or should be avoided in a portability-first project (12).

## 5.3 Comparison

Table 4 scores the mechanisms on the four properties defined in Section 5.1. Portability is scored on whether the value is inside the `.ifc` file. Queryability is scored on whether a generic IFC parser, or a language model with generic tools, is able to find it by name. Interoperability is scored on how many existing viewers and checkers understand the mechanism.

**Table 4** Comparison of the twelve mechanisms on four properties.

| Mechanism | Portability | Queryability | Interoperability | Scalability |
|---|---|---|---|---|
| Custom property sets | High | High | Medium to high | Medium |
| Standard environmental property sets | High | High | Medium | Medium |
| Element quantities | High | High | High | Medium |
| Material properties | High | Medium | Medium | High |
| Spatial aggregates | High | High | Medium | High |
| External dataset reference | Medium | Very high | Medium | Very high |
| Library and classification references | Medium | Medium | Medium to high | High |
| `IfcPerformanceHistory` | Medium | Medium | Low to medium | Medium |
| Constraints, objectives, metrics | Medium | Medium | Low to medium | Medium |
| Custom schema extension | Low | High with custom tools | Low | Medium |

As Table 4 shows, no single mechanism satisfies all four properties. Accordingly, it is recommended that three be used together, each performing the function for which it is best suited.

## 5.4 The three-layer recommendation

**Layer 1: summary values in custom property sets.** It is recommended that the scalar values which people inspect, filter by, colour by, and ask about be written directly into property sets on elements and on spatial containers. One set per topic should be used, so that a viewer's property panel remains readable and an IDS is able to require the topic as a unit:

```text
Pset_NRCEmbodiedCarbon
Pset_NRCOperationalCarbon
Pset_NRCEnergyPerformance
Pset_NRCAnalyticsProvenance
```

Every set carries `ScenarioName` and `AnalysisRunId`, so that a value can never be separated from the run that produced it. Units and lifecycle stages are carried in the property names, as in `EmbodiedCarbon_A1A3_kgCO2e`, so that the meaning survives tools which drop the IFC unit assignment. Annex A gives the full definitions. It should be noted that the aggregate sets written on storeys and on the building currently share the element property names, an arrangement which the unattended run of Section 8.2 showed to be a defect; the correction is stated in Section 9.2.

**Layer 2: a reference to the full dataset.** It is recommended that an `IfcDocumentReference` be attached to the project, or to the building, naming the external result table, its format, its checksum, and the join key. The external table should be long-format, one row per combination of run, element, and metric, so that new metrics never require a schema change:

```text
AnalysisRunId, GlobalId, IfcClass, MetricId, MetricName, Value, Unit,
LifecycleStage, Scenario, Source, Confidence, ComputationMethod
```

Parquet [17] is the recommended format, being columnar, compressed, typed, and loadable into DuckDB, pandas, and every lakehouse tool. CSV is acceptable for small datasets and for human inspection.

**Layer 3: a metric dictionary.** It is recommended that a short list of metric identifiers be defined, and that each property name in Layer 1 and each `MetricId` in Layer 2 be mapped to one of them:

```text
NRC.EC.A1A3.TOTAL       Embodied carbon, stages A1 to A3, kgCO2e
NRC.EC.A1A5.TOTAL       Embodied carbon, stages A1 to A5, kgCO2e
NRC.OC.ANNUAL           Operational carbon, kgCO2e per year
NRC.EUI.ANNUAL          Energy use intensity, kWh per m2 per year
NRC.GWP.MATERIAL_FACTOR Global warming potential factor per material unit
```

The dictionary may be published as an IFC library reference, as a bsDD domain, or simply as a versioned JSON file shipped with the IDS. Its purpose is to give the query layer of Section 7 one place in which to resolve a term such as "carbon" to a column, and to give an IDS one vocabulary to require.

## 5.5 Writing property sets without disturbing the file

Layer 1 requires writing into a client's IFC file, and Section 4.2 noted that most libraries re-serialise the whole file. The toolkit's editing library [29] instead treats the source file as bytes, finds the highest entity identifier and the owner-history entity, and appends new entities. For one element and one property set it emits N `IFCPROPERTYSINGLEVALUE` lines, one `IFCPROPERTYSET`, and one `IFCRELDEFINESBYPROPERTIES`. The `GlobalId` of each new entity is a deterministic hash of a caller-supplied key, so that running the writer twice produces the same bytes.

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

An entity-level diff, `IfcDiff.Compare`, then reports exactly which entities were added, and `IfcPatcher.Remove` removes them again. Section 8.3 reports this round trip verified byte for byte on the Duplex model. The same path is exposed as the `sink.writePsets` node in the dataflow graph, where it runs only inside an explicit run.

The practical consequence for NRC is that an enriched file may be returned to a model author together with a diff that lists the additions and nothing else, and that the author is able to strip the additions and recover the original file exactly.

## 5.6 Recommendation in brief

In summary, it is recommended that six measures be adopted for the storage of analytics:

1. Summary analytics should be written into custom property sets on elements, spaces, storeys, buildings, and the project, using the definitions in Annex A;
2. Units, lifecycle stage, scenario, run identifier, and provenance should appear in every set;
3. The full result table should be referenced from the IFC by an `IfcDocumentReference`, joined on `GlobalId` and stored as Parquet;
4. A small metric dictionary should be published, and every property and metric identifier mapped to it;
5. Writing should be performed by a byte-exact patch rather than a re-serialisation, so that additions are auditable and reversible;
6. Measures 1 to 4 should be expressed as an IDS specification, so that delivered models may be validated.

Measures 1, 3, and 5 are implemented and tested in the toolkit. Measure 4 is a document. Measure 6 remains future work and is discussed in Section 10.2.
