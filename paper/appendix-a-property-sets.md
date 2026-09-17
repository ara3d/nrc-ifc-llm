# Appendix A. Property-set definitions

The Layer 1 property sets recommended in Section 3.4. Names follow IFC conventions: the set
name identifies the topic; each property name carries its lifecycle stage and unit so that the
meaning survives tools that drop unit assignments. All values are `IfcPropertySingleValue`.

Every set includes the two provenance properties `ScenarioName` and `AnalysisRunId`. A value
without them cannot be joined back to the run that produced it and must be treated as
unverified.

## Pset_NRCEmbodiedCarbon

Applies to: `IfcElement` subtypes, `IfcSpace`, `IfcBuildingStorey`, `IfcBuilding`, `IfcProject`.

| Property | IFC type | Unit | Meaning |
|---|---|---|---|
| `EmbodiedCarbon_A1A3_kgCO2e` | `IfcReal` | kgCO2e | Product stage total |
| `EmbodiedCarbon_A1A5_kgCO2e` | `IfcReal` | kgCO2e | Product plus construction stage total |
| `EmbodiedCarbon_kgCO2e_per_m2` | `IfcReal` | kgCO2e/m2 | Intensity over the element's or container's reference area |
| `ReferenceArea_m2` | `IfcReal` | m2 | The area used for the intensity |
| `ScenarioName` | `IfcLabel` | | Scenario identifier |
| `AnalysisRunId` | `IfcIdentifier` | | Run identifier, joins to Layer 2 |

## Pset_NRCOperationalCarbon

Applies to: as above.

| Property | IFC type | Unit | Meaning |
|---|---|---|---|
| `OperationalCarbon_kgCO2e_per_year` | `IfcReal` | kgCO2e/yr | Annual operational emissions attributed to the object |
| `OperationalCarbon_kgCO2e_per_m2_year` | `IfcReal` | kgCO2e/m2/yr | Intensity |
| `GridEmissionFactor_kgCO2e_per_kWh` | `IfcReal` | kgCO2e/kWh | Factor used |
| `ScenarioName` | `IfcLabel` | | |
| `AnalysisRunId` | `IfcIdentifier` | | |

## Pset_NRCEnergyPerformance

Applies to: as above.

| Property | IFC type | Unit | Meaning |
|---|---|---|---|
| `EnergyUseIntensity_kWh_per_m2_year` | `IfcReal` | kWh/m2/yr | Site energy use intensity |
| `AnnualEnergyUse_kWh` | `IfcReal` | kWh | Annual site energy |
| `HeatingEnergy_kWh` | `IfcReal` | kWh | Annual heating end use |
| `CoolingEnergy_kWh` | `IfcReal` | kWh | Annual cooling end use |
| `ScenarioName` | `IfcLabel` | | |
| `AnalysisRunId` | `IfcIdentifier` | | |

## Pset_NRCAnalyticsProvenance

Applies to: `IfcProject`, and optionally any object that carries one of the sets above.

| Property | IFC type | Meaning |
|---|---|---|
| `AnalysisRunId` | `IfcIdentifier` | Run identifier |
| `SourceTool` | `IfcLabel` | Tool name and version |
| `Methodology` | `IfcLabel` | Standard or method (for example EN 15978) |
| `ComputedAt` | `IfcLabel` | ISO 8601 timestamp, UTC |
| `ComputedBy` | `IfcLabel` | Person or organisation |
| `MetricDictionaryVersion` | `IfcLabel` | Version of the Layer 3 dictionary |
| `ResultDatasetURI` | `IfcText` | Location of the Layer 2 table |
| `ResultDatasetFormat` | `IfcLabel` | `Parquet`, `CSV`, or `DuckDB` |
| `ResultDatasetChecksum` | `IfcLabel` | SHA-256 of the table file |
| `JoinKey` | `IfcLabel` | `GlobalId` |

## Ara3D_Compliance

The set used in case study B to record a verdict and a human override on an element. Included
here because it follows the same pattern and was verified in the round-trip test.

| Property | IFC type | Meaning |
|---|---|---|
| `Verdict` | `IfcLabel` | Verdict produced by the checker |
| `OverrideVerdict` | `IfcLabel` | Verdict asserted by the reviewer |
| `OverrideReason` | `IfcText` | Justification |
| `ReviewedBy` | `IfcLabel` | Reviewer |

A production version should add `RuleId`, `Citation`, `CheckedAt`, and `RuleFileChecksum`.

## Example STEP output

The lines appended for one element by the writer in Section 3.5, ids relative to the file's
highest existing id:

```text
#38899=IFCPROPERTYSINGLEVALUE('EmbodiedCarbon_A1A3_kgCO2e',$,IFCREAL(412.7),$);
#38900=IFCPROPERTYSINGLEVALUE('ScenarioName',$,IFCLABEL('Baseline'),$);
#38901=IFCPROPERTYSINGLEVALUE('AnalysisRunId',$,IFCIDENTIFIER('run-2026-07-14-01'),$);
#38902=IFCPROPERTYSET('1kQ7x$...',#41,'Pset_NRCEmbodiedCarbon',$,(#38899,#38900,#38901));
#38903=IFCRELDEFINESBYPROPERTIES('2mR8y$...',#41,$,$,(#1234),#38902);
```

The two `GlobalId` literals are deterministic hashes of the caller's key, so a second run
produces the same five lines.
