Discussion with ChatGTP on July 8th:

```The NRC produces analytics on building models (operational carbon, embodied carbon, energy, and other performance indicators) in workflows external to IFC. The NRC wishes to explore how these analytics can be: stored inside IFC so the data is portable, reusable, and queryable. Brainstorm different options about how this kind of data can be stored within an IFC and describe the pros and cons.```

# Storing Analytics in IFC

Assuming IFC 4.x/4.3, there are several viable patterns. The best answer is probably **not one mechanism**, but a hybrid: store the most important, stable summary values directly in IFC property sets, and link to richer external analytical datasets for provenance, recalculation, time series, and bulk query.

IFC 4.3.2 documentation is the current useful reference point; buildingSMART notes that the 4.3.2 docs elaborate the ISO IFC 4.3 release without schema changes. ([ifc43-docs.standards.buildingsmart.org][1])

## 1. Custom IFC property sets on elements

Attach a custom property set, for example:

`Pset_NRCAnalytics`

to `IfcWall`, `IfcSlab`, `IfcWindow`, `IfcSpace`, `IfcBuildingStorey`, `IfcBuilding`, etc., using `IfcRelDefinesByProperties`. IFC explicitly supports assigning property set definitions to occurrence objects or to object types, and the same relationship can associate one or more property sets with one or more objects. ([ifc43-docs.standards.buildingsmart.org][2])

Example properties:

```text
EmbodiedCarbon_A1A3_kgCO2e
EmbodiedCarbon_A1A5_kgCO2e
OperationalCarbon_kgCO2e_per_year
EnergyUseIntensity_kWh_per_m2_year
GWP_kgCO2e
AnalysisScenario
AnalysisRunId
AnalysisDate
SourceTool
Methodology
Confidence
```

Use `IfcPropertySingleValue` for scalar values; it supports a property name, optional description, nominal value, and optional unit override. ([ifc43-docs.standards.buildingsmart.org][3])

**Pros**

This is the simplest and most interoperable approach. It is easy to generate, easy to inspect, and easy to query with almost any IFC parser. It also maps well to visualization: “color all elements by `EmbodiedCarbon_A1A3_kgCO2e`.”

**Cons**

It can become messy quickly. Property names become de facto schema. If every tool invents different names, units, lifecycle-stage conventions, and calculation methods, the data is portable syntactically but not semantically. It is also poor for detailed provenance, uncertainty ranges, multi-scenario results, or time series.

**Best use**

Element-level and spatial-level KPI values that should travel with the model.

---

## 2. Standard environmental property sets where applicable

IFC already contains sustainability-related property set definitions, including `Pset_EnvironmentalImpactIndicators`, which is intended for environmental impact indicators related to a functional unit. ([ifc43-docs.standards.buildingsmart.org][4])

**Pros**

This is more standards-aligned than inventing everything from scratch. It gives the NRC proposal a stronger “openBIM” story and reduces the risk of creating a purely proprietary convention.

**Cons**

The standard property sets may not match NRC’s exact analytics. They may be closer to product/functional-unit environmental indicators than project-specific operational-carbon or analysis-run results. Tool support may also be inconsistent.

**Best use**

Use standard IFC environmental properties where they fit, then add an NRC namespace for values that are not covered cleanly.

Example:

```text
Pset_EnvironmentalImpactIndicators
Pset_NRCAnalytics
Pset_NRCAnalyticsProvenance
```

---

## 3. Quantities via `IfcElementQuantity`

`IfcElementQuantity` is intended for derived physical measures of elements, such as quantities associated with buildings, storeys, spaces, walls, slabs, and finishes. It is assigned through `IfcRelDefinesByProperties`. ([ifc43-docs.standards.buildingsmart.org][5])

**Pros**

This is a natural fit for things like area, volume, mass, count, length, and other takeoff quantities that analytics depend on. It gives the calculation chain a clean structure: geometry/material quantities first, carbon/energy results second.

**Cons**

Carbon and energy performance values are not always “quantities” in the takeoff sense. Forcing all analytics into quantity sets can blur the distinction between measured/derived physical quantities and analytical results.

**Best use**

Store supporting takeoff quantities, not necessarily the final carbon result.

Example:

```text
Qto_NRCBaseQuantities
  NetVolume_m3
  NetArea_m2
  MaterialMass_kg
  ExposedArea_m2

Pset_NRCAnalytics
  EmbodiedCarbon_A1A3_kgCO2e
```

---

## 4. Material-level properties

For embodied carbon, a strong option is to store environmental factors and assumptions on IFC materials, not only on elements. IFC supports `IfcMaterialProperties`, which assigns a set of named material properties, each with value and unit, to material definitions. ([ifc43-docs.standards.buildingsmart.org][6])

Example material properties:

```text
Density_kg_per_m3
GWP_A1A3_kgCO2e_per_kg
GWP_A1A3_kgCO2e_per_m3
EPDReference
EPDDeclaredUnit
EPDExpiryDate
DataQuality
```

**Pros**

This avoids duplicating the same carbon factors on every wall, slab, or beam. It also makes the model more reusable: a downstream system can recompute results if quantities change.

**Cons**

IFC material data is often incomplete, inconsistent, or too generic. Many models have material names like “Concrete - Cast-in-Place” without enough specificity for LCA. Also, the final result still depends on element geometry, quantities, waste factors, transport assumptions, lifecycle stages, and calculation method.

**Best use**

Store reusable environmental factors and EPD references on materials; store computed totals on elements/spaces/buildings.

---

## 5. Store summaries at multiple aggregation levels

Analytics often need to be queried at different scales:

```text
IfcElement        → per-object carbon/energy contribution
IfcSpace          → room-level allocation
IfcBuildingStorey → floor-level total
IfcBuilding       → building-level total
IfcProject        → portfolio/project-level summary
IfcZone           → department, use type, thermal zone, renovation phase
```

**Pros**

This is very useful for dashboards and LLM queries. A user can ask, “Which floor has the highest embodied carbon?” without summing every element live.

**Cons**

You now have redundant data. If an element-level value changes, the space/storey/building totals may become stale unless you store run IDs, timestamps, and a clear aggregation method.

**Best use**

Store both fine-grained values and cached aggregates, but include provenance fields:

```text
AnalysisRunId
AggregationSource
AggregationDate
AggregationMethod
IncludesElementsCount
```

---

## 6. External analytics dataset referenced from IFC

Instead of storing all analytics directly inside IFC, store a reference to an external CSV, JSON, Parquet, DuckDB, web endpoint, or report. IFC supports document references: `IfcDocumentReference` is a reference to a document location, and `IfcRelAssociatesDocument` can associate document information with objects or object types. ([ifc43-docs.standards.buildingsmart.org][7])

Example IFC-side properties:

```text
Pset_NRCAnalyticsReference
  AnalysisRunId
  ResultDatasetURI
  ResultDatasetFormat = "Parquet"
  JoinKey = "GlobalId"
  DatasetChecksum
  SchemaVersion
```

External table:

```text
GlobalId, MetricName, Value, Unit, Scenario, LifecycleStage, Source, Confidence
```

**Pros**

This is much more scalable. It supports rich tables, multiple scenarios, time series, uncertainty distributions, provenance, and fast querying in DuckDB/Parquet. It also aligns well with Ara 3D / BIM Lakehouse workflows.

**Cons**

The data is not fully self-contained unless the external file is packaged with the IFC. Links can break. Some stakeholders may object that this is not truly “stored inside IFC,” even though the IFC contains the association and lookup metadata.

**Best use**

Use this for full analytical datasets. Store only the most important summary values directly in IFC.

---

## 7. IFC library references for reusable analytical definitions

IFC supports library metadata through `IfcLibraryInformation`, which describes an external structured information store that supports lookup by index/reference and can include name, description, version, publisher, and location. ([ifc43-docs.standards.buildingsmart.org][8])

This could reference:

```text
NRC carbon-factor library
NRC metric dictionary
EPD database
Energy model result schema
National benchmark table
```

**Pros**

Good for separating the *definition* of a metric from the *value* of a metric. For example, the IFC value might say:

```text
MetricId = "NRC.EMBODIED_CARBON.A1A3"
Value = 1234.5
Unit = "kgCO2e"
```

and the library explains exactly what that metric means.

**Cons**

Still depends on external governance. The reference is only useful if the library is maintained and resolvable.

**Best use**

Metric dictionaries, carbon factor libraries, EPD references, benchmark definitions, and LLM-friendly semantic lookup.

---

## 8. Classification references / bsDD-style semantic tagging

IFC can associate classification items with objects through `IfcRelAssociatesClassification`, and `IfcClassificationReference` represents a reference into a classification system. ([ifc43-docs.standards.buildingsmart.org][9])

This is useful for tagging elements, spaces, systems, materials, or metrics with a controlled vocabulary.

Example:

```text
Classification: NRC Analytics Metric Dictionary
Reference: NRC.EC.A1A3.TOTAL
Name: Embodied Carbon A1-A3 Total
```

**Pros**

Improves semantic consistency. Helps LLMs map natural language to the correct field. Also helps downstream systems understand that `GWP`, `EmbodiedCarbon`, and `kgCO2e_A1A3` may refer to related concepts.

**Cons**

Classification is not a good place to store numeric results. It identifies what something is; it does not carry rich analytical values by itself.

**Best use**

Use classification references to define metric identity, material categories, space-use types, lifecycle stages, and analysis categories.

---

## 9. `IfcPerformanceHistory` for operational or time-based performance

`IfcPerformanceHistory` is specifically intended to document actual performance of an occurrence over time, including machine-measured data, human-specified data, predictions, and simulations. ([ifc43-docs.standards.buildingsmart.org][10])

Potential uses:

```text
Monthly operational energy
Hourly energy simulation result
Measured indoor temperature
Predicted operational carbon
Post-occupancy performance indicators
```

**Pros**

This is semantically closer to operational performance than a flat property set. It distinguishes static BIM attributes from actual/predicted/simulated performance history.

**Cons**

It is more complex and likely less supported by common BIM tools. For a lightweight prototype, it may be overkill.

**Best use**

Use for operational analytics, time series, simulations, and measured building performance where IFC semantic correctness matters.

---

## 10. Constraints, objectives, and metrics

IFC includes `IfcMetric`, which is used to capture quantitative resultant metrics that can be applied to objectives. ([ifc43-docs.standards.buildingsmart.org][11]) Constraint associations can be applied to IFC root objects through `IfcRelAssociatesConstraint`. ([ifc43-docs.standards.buildingsmart.org][12])

Example:

```text
Objective: Meet NRC embodied carbon target
Metric: EmbodiedCarbon_A1A3 <= 350 kgCO2e/m2
Result: Pass / Fail
```

**Pros**

Good for compliance, benchmarking, targets, and pass/fail analytics. This can express not just “what is the value?” but “does the model satisfy a requirement?”

**Cons**

Not a great place for bulk raw analytics. More useful for high-level evaluation results than for detailed element-level datasets.

**Best use**

Regulatory checks, carbon targets, energy targets, design objectives, and compliance summaries.

---

## 11. Store visualization-oriented metadata

For display, one could store color categories, labels, or annotation metadata:

```text
CarbonColorClass = "High"
CarbonColorRGB = "255,0,0"
CarbonLabel = "High embodied carbon"
```

This can be attached through custom property sets or possibly represented as annotation/presentation data.

**Pros**

Very useful for demonstration: an IFC viewer can color-code geometry by result class.

**Cons**

Color is not the analytic result. If you only store visualization state, the model becomes less useful for recalculation and querying. Color scales can also be misleading unless the thresholds are stored.

**Best use**

Store visualization as derived metadata, not as the primary analytical record.

Recommended pattern:

```text
EmbodiedCarbon_A1A3_kgCO2e = 1234.5
CarbonIntensityClass = "High"
ColorMap = "NRC_Default_EmbodiedCarbon_2026"
ColorBinMin = 1000
ColorBinMax = 2000
```

---

## 12. Custom IFC schema extension

You could define custom entities such as:

```text
IfcCarbonAnalysisResult
IfcEnergyAnalysisResult
IfcAnalyticsScenario
IfcAnalyticsRun
```

**Pros**

This gives a clean, rigorous data model. You can represent scenarios, provenance, uncertainty, lifecycle stages, and result tables properly.

**Cons**

This is the worst option for interoperability. Most IFC tools will not understand custom entities unless they are built against the extension. It risks creating an NRC-specific IFC dialect.

**Best use**

Research prototype only, unless the goal is to contribute to future IFC/bSDD/IDS standardization.

---

# Recommended NRC proposal approach

For the NRC project, I would propose a **three-layer strategy**.

## Layer 1: Direct IFC summary properties

Add custom property sets to elements and spatial containers:

```text
Pset_NRCAnalytics
Pset_NRCEmbodiedCarbon
Pset_NRCOperationalCarbon
Pset_NRCEnergyPerformance
Pset_NRCAnalyticsProvenance
```

These contain the most important scalar values for display, filtering, and natural-language querying.

Example:

```text
EmbodiedCarbon_A1A3_kgCO2e
EmbodiedCarbon_A1A5_kgCO2e
EmbodiedCarbon_kgCO2e_per_m2
OperationalCarbon_kgCO2e_per_year
EnergyUseIntensity_kWh_per_m2_year
ScenarioName
AnalysisRunId
Methodology
SourceTool
ComputedAt
```

This is the best demo path because it is simple, visible, and queryable.

## Layer 2: IFC references to rich external datasets

Attach an `IfcDocumentReference` or library reference to a richer result table. Use `GlobalId` as the join key. This gives NRC a path to Parquet/DuckDB/CSV/JSON without bloating the IFC.

Example external schema:

```text
AnalysisRunId
GlobalId
IfcClass
MetricId
MetricName
Value
Unit
LifecycleStage
Scenario
Source
Confidence
ComputationMethod
```

This is the best serious-data path.

## Layer 3: Semantic definitions and validation

Define a small NRC metric dictionary:

```text
NRC.EC.A1A3.TOTAL
NRC.EC.A1A5.TOTAL
NRC.OC.ANNUAL
NRC.EUI.ANNUAL
NRC.GWP.MATERIAL_FACTOR
```

Then map IFC property names to these metric IDs using classification/library references where useful. This makes LLM querying much more reliable.

# Practical ranking

| Option                            | Portability |                  Queryability | Interoperability | Scalability | Best for                                |
| --------------------------------- | ----------: | ----------------------------: | ---------------: | ----------: | --------------------------------------- |
| Custom property sets              |        High |                          High |      Medium-high |      Medium | Prototype, viewer, LLM Q&A              |
| Standard environmental Psets      |        High |                          High |           Medium |      Medium | Standards-aligned LCA fields            |
| Element quantities                |        High |                          High |             High |      Medium | Takeoff inputs                          |
| Material properties               |        High |                        Medium |           Medium |        High | Carbon factors, EPD data                |
| Spatial aggregates                |        High |                          High |           Medium |        High | Dashboards                              |
| External dataset reference        |      Medium |                     Very high |           Medium |   Very high | Rich analytics, time series, provenance |
| Library/classification references |      Medium |                        Medium |      Medium-high |        High | Semantic definitions                    |
| `IfcPerformanceHistory`           |      Medium |                        Medium |       Low-medium |      Medium | Operational/time-series performance     |
| Constraints/objectives/metrics    |      Medium |                        Medium |       Low-medium |      Medium | Targets, compliance, pass/fail          |
| Custom IFC schema extension       |         Low | High if custom tooling exists |              Low |      Medium | Research, future standardization        |

# My strongest recommendation

1. **Write summary analytics into IFC property sets** for elements, spaces, storeys, buildings, and project.
2. **Use explicit units, lifecycle stages, scenario names, run IDs, and provenance fields.**
3. **Reference a richer external analytics table** using `IfcDocumentReference`, joined by `GlobalId`.
4. **Define a small NRC metric dictionary** so natural-language queries map reliably to metric IDs.
5. **Optionally test one advanced IFC-native pattern**, such as material-level GWP factors or `IfcPerformanceHistory`, as a comparison.

That gives NRC a concrete prototype, a standards-aware roadmap, and a realistic way to keep IFC portable without pretending that a STEP file is the best place for large analytical datasets.

[1]: https://ifc43-docs.standards.buildingsmart.org/?utm_source=chatgpt.com "IFC 4.3.2 Documentation - buildingSMART International"
[2]: https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcRelDefinesByProperties.htm?utm_source=chatgpt.com "5.1.3.38 IfcRelDefinesByProperties - IFC 4.3.2 Documentation"
[3]: https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcPropertySingleValue.htm?utm_source=chatgpt.com "8.16.3.12 IfcPropertySingleValue - IFC 4.3.2 Documentation"
[4]: https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/Pset_EnvironmentalImpactIndicators.htm?utm_source=chatgpt.com "5.4.4.14 Pset_EnvironmentalImpactIndicators - IFC4.3"
[5]: https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcElementQuantity.htm?utm_source=chatgpt.com "5.4.3.21 IfcElementQuantity - IFC 4.3.2 Documentation - IFC4.3"
[6]: https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcMaterialProperties.htm?utm_source=chatgpt.com "8.10.3.16 IfcMaterialProperties - IFC 4.3.2 Documentation"
[7]: https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcRelAssociatesDocument.htm?utm_source=chatgpt.com "5.1.3.31 IfcRelAssociatesDocument - IFC 4.3.2 Documentation"
[8]: https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcLibraryInformation.htm?utm_source=chatgpt.com "8.6.3.9 IfcLibraryInformation - IFC 4.3.2 Documentation - IFC4.3"
[9]: https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcRelAssociatesClassification.htm?utm_source=chatgpt.com "5.1.3.30 IfcRelAssociatesClassification - IFC 4.3.2 ... - IFC4.3"
[10]: https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcPerformanceHistory.htm?utm_source=chatgpt.com "5.2.3.1 IfcPerformanceHistory - IFC 4.3.2 Documentation"
[11]: https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcMetric.htm?utm_source=chatgpt.com "8.3.3.2 IfcMetric - IFC 4.3.2 Documentation - IFC4.3"
[12]: https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcRelAssociatesConstraint.htm?utm_source=chatgpt.com "5.2.3.3 IfcRelAssociatesConstraint - IFC 4.3.2 Documentation - IFC4.3"
