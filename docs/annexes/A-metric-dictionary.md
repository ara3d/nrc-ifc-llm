# Annex A: Metric dictionary

This annex lists the metric dictionary the proof of concept stores beside the analytics: one row per metric and level, naming the property set and property that hold the value. Source: `samples/nrc/nrc-metrics.csv` (metric dictionary) and `samples/nrc/nrc-run.csv` (run facts), from the development clone of the BIM Open Toolkit, `bim-open-toolkit` at commit 6f37755, the content of the coming tag `v0.2`. Every analytics value in this annex is synthetic: the proof of concept generates it, and it does not describe a real building.

## Naming rule

User-defined property sets are named with the prefix `NRC_`, not `Pset_`. The IFC standard reserves the `Pset_` prefix for property sets that buildingSMART defines, so a user-defined set that used it would claim to be part of the standard. The earlier version of the proof of concept (toolkit tag `v0.1`) used `Pset_NRC*` names; the coming tag `v0.2` renames them to `NRC_*`. Property names keep their unit in the name, for example `OperationalCarbon_kgCO2e_per_year`.

## Columns

`MetricId` is the stable identifier of a metric and is shared by its element, storey, zone, and building rows. `Level` says what the value describes. `PropertySet` and `PropertyName` name where the value is stored in the IFC file. `ValueType` is the IFC value type. `Unit` is the unit of the value. `LifecycleStage` is the EN 15978 stage the value belongs to (blank when the metric has none). `Rollup` is how a higher level is computed from the level below: `none` (stored per element), `sum`, `mean`, `count`, or `ratio:A/B` (metric A divided by metric B, both at the same level). `Description` is free text. `Decimals` is the rounding of a rolled-up value, blank where the value is stored as supplied.

## Element level

| MetricId | Level | PropertySet | PropertyName | ValueType | Unit | LifecycleStage | Rollup | Description | Decimals |
|---|---|---|---|---|---|---|---|---|---|
| NRC.EC.A1A3.TOTAL | element | NRC_EmbodiedCarbon | EmbodiedCarbon_A1A3_kgCO2e | Real | kgCO2e | A1-A3 | none | Embodied carbon of the element's production stage (synthetic) |  |
| NRC.EC.A1A5.TOTAL | element | NRC_EmbodiedCarbon | EmbodiedCarbon_A1A5_kgCO2e | Real | kgCO2e | A1-A5 | none | Embodied carbon up to construction (synthetic) |  |
| NRC.OC.ANNUAL | element | NRC_OperationalCarbon | OperationalCarbon_kgCO2e_per_year | Real | kgCO2e/yr | B6 | none | Annual operational carbon attributed to the element (synthetic) |  |
| NRC.GRID.FACTOR | element | NRC_OperationalCarbon | GridEmissionFactor_kgCO2e_per_kWh | Real | kgCO2e/kWh | B6 | none | Grid emission factor the operational carbon was computed with; one value per run, taken from nrc-run.csv (synthetic) |  |
| NRC.EUI.ANNUAL | element | NRC_EnergyPerformance | EnergyUseIntensity_kWh_per_m2_year | Real | kWh/m2/yr | B6 | none | Annual energy use intensity attributed to the element (synthetic) |  |

## Storey level

| MetricId | Level | PropertySet | PropertyName | ValueType | Unit | LifecycleStage | Rollup | Description | Decimals |
|---|---|---|---|---|---|---|---|---|---|
| NRC.COUNT.ELEMENTS | storey | NRC_StoreySummary | ElementCount | Integer | count |  | count | Analysed elements on the storey | 0 |
| NRC.EC.A1A3.TOTAL | storey | NRC_StoreySummary | TotalEmbodiedCarbon_A1A3_kgCO2e | Real | kgCO2e | A1-A3 | sum | Sum of element A1-A3 embodied carbon on the storey | 1 |
| NRC.EC.A1A5.TOTAL | storey | NRC_StoreySummary | TotalEmbodiedCarbon_A1A5_kgCO2e | Real | kgCO2e | A1-A5 | sum | Sum of element A1-A5 embodied carbon on the storey | 1 |
| NRC.OC.ANNUAL | storey | NRC_StoreySummary | TotalOperationalCarbon_kgCO2e_per_year | Real | kgCO2e/yr | B6 | sum | Sum of element operational carbon on the storey | 1 |
| NRC.EUI.ANNUAL | storey | NRC_StoreySummary | MeanEnergyUseIntensity_kWh_per_m2_year | Real | kWh/m2/yr | B6 | mean | Mean of element energy use intensity on the storey (element-count mean; synthetic data has no areas) | 2 |

## Zone level

| MetricId | Level | PropertySet | PropertyName | ValueType | Unit | LifecycleStage | Rollup | Description | Decimals |
|---|---|---|---|---|---|---|---|---|---|
| NRC.COUNT.SPACES | zone | NRC_ZoneSummary | SpaceCount | Integer | count |  | count | Conditioned spaces in the zone | 0 |
| NRC.AREA.FLOOR | zone | NRC_ZoneSummary | TotalFloorArea_m2 | Real | m2 |  | sum | Sum of the zone's space floor areas (GSA BIM Area quantity of each IfcSpace) | 1 |
| NRC.ENERGY.ANNUAL | zone | NRC_ZoneSummary | TotalOperationalEnergy_kWh_per_year | Real | kWh/yr | B6 | sum | Sum of the zone's space annual operational energy (synthetic) | 1 |
| NRC.OC.ANNUAL | zone | NRC_ZoneSummary | TotalOperationalCarbon_kgCO2e_per_year | Real | kgCO2e/yr | B6 | sum | Sum of the zone's space annual operational carbon: energy times the grid emission factor (synthetic) | 1 |
| NRC.EUI.ANNUAL | zone | NRC_ZoneSummary | ZoneEnergyUseIntensity_kWh_per_m2_year | Real | kWh/m2/yr | B6 | ratio:NRC.ENERGY.ANNUAL/NRC.AREA.FLOOR | Zone energy divided by the zone's floor area (area-weighted; synthetic) | 2 |

## Building level

| MetricId | Level | PropertySet | PropertyName | ValueType | Unit | LifecycleStage | Rollup | Description | Decimals |
|---|---|---|---|---|---|---|---|---|---|
| NRC.COUNT.ELEMENTS | building | NRC_BuildingSummary | ElementCount | Integer | count |  | count | Analysed elements in the building | 0 |
| NRC.EC.A1A3.TOTAL | building | NRC_BuildingSummary | TotalEmbodiedCarbon_A1A3_kgCO2e | Real | kgCO2e | A1-A3 | sum | Sum of element A1-A3 embodied carbon in the building | 1 |
| NRC.EC.A1A5.TOTAL | building | NRC_BuildingSummary | TotalEmbodiedCarbon_A1A5_kgCO2e | Real | kgCO2e | A1-A5 | sum | Sum of element A1-A5 embodied carbon in the building | 1 |
| NRC.OC.ANNUAL | building | NRC_BuildingSummary | TotalOperationalCarbon_kgCO2e_per_year | Real | kgCO2e/yr | B6 | sum | Sum of element operational carbon in the building | 1 |
| NRC.EUI.ANNUAL | building | NRC_BuildingSummary | MeanEnergyUseIntensity_kWh_per_m2_year | Real | kWh/m2/yr | B6 | mean | Mean of element energy use intensity in the building (element-count mean) | 2 |

## Run facts

The dictionary file names the run that produced the values; the facts of that run are written into the IFC file as the `NRC_AnalyticsProvenance` property set on the project.

| Field | ValueType | Value |
|---|---|---|
| AnalysisRunId | Identifier | run-2026-09-17-01 |
| ScenarioName | Label | Baseline |
| GridEmissionFactor_kgCO2e_per_kWh | Real | 0.11 |
| SourceTool | Label | nrc-ifc-llm/poc/generate_synthetic_analytics.py |
| Methodology | Label | Synthetic, illustrative; not EN 15978 |
| ComputedAt | Label | 2026-09-17T00:00:00Z |
| ComputedBy | Label | Ara 3D |
| MetricDictionaryVersion | Label | NRC-metrics-0.2 |
| MetricDictionaryURI | Text | nrc-metrics.csv |
| ResultDatasetURI | Text | nrc_analytics_long.csv |
| ResultDatasetFormat | Label | CSV |
| JoinKey | Label | GlobalId |

