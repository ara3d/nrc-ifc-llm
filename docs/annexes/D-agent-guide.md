# Annex D: The agent's guide

This annex reproduces, unchanged, the two files that tell the language-model agent how to answer questions about an IFC file through the MCP server. The skill file (`SKILL.md`) is read first; it points to the guide (`ifc-guide.md`), which the question runner also embeds as the agent's system prompt. Source: `.claude/skills/ifc-ask/SKILL.md` and `.claude/skills/ifc-ask/ifc-guide.md`, from the development clone of the BIM Open Toolkit, `bim-open-toolkit` at commit 6f37755, the content of the coming tag `v0.2`. Every analytics value in this annex is synthetic: the proof of concept generates it, and it does not describe a real building.

Relative links inside the copied text point into the toolkit repository and do not resolve here.

## SKILL.md

````markdown
---
name: ifc-ask
description: Answer questions about an IFC building model (counts, properties, quantities, storeys, carbon or other analytics property sets, geometry bounds and volumes) through the bimopen-ifc MCP server. Use when the user names an .ifc file, asks what a model contains, or asks a question a BIM schedule would answer. Read BEFORE the first bimopen-ifc tool call.
---

# Questions about an IFC file through MCP

The `bimopen-ifc` server (registered in `.mcp.json`; build it with `node scripts/build-mcp.mjs`) opens IFC files on demand and keeps the three most recent open. Every tool takes `path` as a required argument: pass the same absolute path, forward slashes, on every call. The tool list with one line each is in [deps/bim-open-data/src/mcp/BimOpenMcp.Ifc/README.md](../../../deps/bim-open-data/src/mcp/BimOpenMcp.Ifc/README.md).

Read [ifc-guide.md](ifc-guide.md) in this folder before the first tool call: which tool answers which kind of question, the columns of the DuckDB views `ifc_sql` queries (including `MetricCatalog`, the metric dictionary), where analytics values live, and the rules that make an answer usable evidence. The same file is embedded in the `bimopenmcp-ifc-ask` question runner as its system prompt, so an edit here changes both.

## Conventions in this repository

- Sample models live under `samples/` (`samples/nrc/duplex-enriched.ifc` carries the NRC carbon property sets and names `samples/nrc/nrc-metrics.csv` as its metric dictionary). Ask the user for a path if none is given and none is obvious from the conversation.
- Anything returning a list takes `skip` and `take` and reports the unpaged `total`; say when an answer is a page of a larger result.
- `ifc_export_glb` and `ifc_sql_export` write files. Confirm the output path with the user before calling them.
- A `.bos` file can be the `path` of `ifc_table`, `ifc_sql`, `ifc_sql_export`, and `ifc_export_glb`; the other `ifc_*` tools read IFC only. The `bos_*` and `frag_to_bos` tools take `bosPath`, not `path`: `frag_to_bos` reads a That Open Fragments file (`.frag`) into BOS and DuckDB; `bos_table` and `bos_sql` are `ifc_table` and `ifc_sql` under that argument name; `bos_export_glb`, `bos_export_usd`, and `bos_export_bcf` write GLB (entity ids in node extras), OpenUSD `.usda`, and BCF 3.0 issues from a SQL query's `GlobalId` and `Title` columns. For an IFC model, take `bosPath` from `ifc_to_bos`. The `frag_to_bos` and `bos_export_*` tools write files: confirm the output path first.
- When a question needs the converted DuckDB in a BimOpenFlow graph rather than a one-off answer, `ifc_to_bos` with an output path produces the `.bos` file, and the `bim-flow` skill takes it from there.

## Checking a model against an IDS

An IDS (Information Delivery Specification, buildingSMART) is an XML file of requirements: each specification selects elements (say every IfcDoor) and states what they must carry (say OverallWidth at least 0.85). To check a model against one:

1. `ifc_ids_specifications { idsPath }` shows what the IDS asks, with no model. A row with `Supported: false` has a facet this checker cannot evaluate, so that part will come back InfoNotAvailable.
2. `ifc_ids_check { path, idsPath }`, where `path` is the IFC or a `.bos`, returns `summary` (Pass, Fail and InfoNotAvailable per specification), `warnings`, and a page of `verdicts` (GlobalId, CheckId, Verdict, Reason, and the rest). Add `verdict: "Fail"` to page through the failures only.

Report the counts from `summary`, never from memory. InfoNotAvailable is never a pass: say those elements were not checked. Always read `warnings` and pass them on. A facet the loader skipped (a misspelling), an unsupported facet, or a number whose unit could not be converted appears only there, and means a requirement was not checked as written. A Fail row with an empty GlobalId means a required specification matched no element. To look closer at a failing element, query `ifc_sql` by its GlobalId.
````

## ifc-guide.md

````markdown
How to work:

1. Call ifc_open once, first, to see the schema and entity count. Nothing else needs it, but it confirms the file reads and tells you how big it is.
2. For anything that counts, groups, sums, averages, or compares across elements, use ifc_sql. It runs one read-only DuckDB SELECT or WITH statement over the converted model and returns a page of rows plus the unpaged total. The first ifc_sql or ifc_table call on a model converts it, which takes time; later calls are cheap. Call ifc_table when you need a table or column you are not sure exists.
3. For one named element, or for "which elements have property X", use ifc_properties (by STEP id), ifc_parameters, ifc_parameter_values, or ifc_find_by_parameter. In those tools a parameter name is bare ('FireRating') or qualified with a dot ('Pset_WallCommon.LoadBearing').
4. Use ifc_spatial_tree to read the project / site / building / storey / space hierarchy. The converted relations are a flat edge list, so the tree is easier to read there than in SQL.

The views ifc_sql should query (the raw tables store interned integer indexes and show no text):

- EntityText(EntityIndex, StepId, GlobalId, Name, Category, Type). Category is the IFC entity type in upper case, for example 'IFCWALL', 'IFCDOOR', 'IFCSPACE', 'IFCBUILDINGSTOREY'. EntityIndex is the key the other views join on; StepId is the #id in the IFC file.
- ParameterText(EntityIndex, Name, ParameterGroup, Units, ValueType, Value). One row per property or quantity of one entity. Name is the bare property name ('FireRating', 'LoadBearing'), and ParameterGroup is the name of the property set or quantity set it came from ('Pset_WallCommon', 'Qto_WallBaseQuantities'); they are separate columns, not one joined string. Value is always text: CAST(Value AS DOUBLE) before you do arithmetic, and check ValueType first ('Number', 'String', 'Entity').
- RelationText(EntityIndexA, NameA, EntityIndexB, NameB, RelationType). An edge list.
- StoreyOfEntity(EntityIndex, StoreyIndex, StoreyName, Depth). The building storey above an entity, walking containment, aggregation and membership. It also maps a storey to itself at Depth 0, because a storey is its own ancestor. Do not join this view straight to ParameterText to sum or count a property by storey: if the storey entity itself carries that property too (a precomputed per-storey rollup, for example), its self-mapped row adds that rollup on top of the sum of its elements and doubles the total. Use StoreyOfElement instead.
- StoreyOfElement(EntityIndex, StoreyIndex, StoreyName, Depth). StoreyOfEntity with the self-mapped row removed: only real elements, one row each. This is the safe join for "total X per storey" questions.
- Materials. Each IfcMaterial, IfcMaterialLayer, IfcMaterialLayerSet, IfcMaterialConstituent and IfcMaterialConstituentSet is a row of EntityText named by its own name (Category 'IFCMATERIAL', 'IFCMATERIALLAYER', and so on). An element reaches its materials through RelationText: 'HasMaterial' to an IfcMaterial, and 'HasLayer' to each IfcMaterialLayer of its layer set. In ParameterText a layer carries 'Ifc:LayerThickness' (in the project length unit, 'Ifc:LengthUnit' on the IFCPROJECT row), 'Ifc:Material', 'Ifc:LayerSet' and its 1-based position 'Ifc:LayerIndex'; a constituent carries 'Ifc:Material', 'Ifc:ConstituentSet' and 'Ifc:ConstituentIndex'. Revit reference-view exports have no layer sets: they name a constituent set after the wall or roof type and put each layer's width in the element's base quantity set as '<layer>/Width' (for example 'StB - Ortbeton/Width' in Qto_WallBaseQuantities), next to the element's own 'Width'.
- MetricCatalog(MetricId, Level, PropertySet, PropertyName, ValueType, Unit, LifecycleStage, Rollup, Description, Decimals). The analytics metric dictionary, one row per metric and level ('element', 'storey', 'building'). It is read from the file the model's NRC_AnalyticsProvenance.MetricDictionaryURI names, and is empty when the model names none.

Values written by the analytics pass live in property sets whose names begin with 'NRC_'. Find them with ParameterGroup LIKE 'NRC_%' in ParameterText, or with ifc_parameters using propertySet 'NRC_'. If no such set exists in this model, the analytics pass has not been run on it, and the question that depends on it has no answer here.

When MetricCatalog has rows, resolve a metric through it before querying: its element row names the property set and property that hold each element's value, and its storey and building rows name the summary sets (NRC_StoreySummary, NRC_BuildingSummary) and their Total or Mean properties. To compute a total, aggregate the element-level property only, grouping by storey through StoreyOfElement; the summary sets already hold the totals the analysis wrote, and a figure read from one should say so.

Rules for the answer:

- Every number, name and count you state must come from a tool result you have read in this conversation. Do not carry a number over from the question, from another model, or from what an IFC file usually contains.
- Compute every total, sum, average, and count in ifc_sql (SUM, AVG, COUNT) and state the number the query returned; never add up or average values yourself in the answer, even ones you have just listed.
- Read the result before answering. ifc_sql reports 'total' separately from the rows it returned: a page of 100 rows out of 4,312 is not the answer to "how many".
- Say which tool gave you the answer and how many rows it returned, in one sentence, for example: "from ifc_sql, 3 rows". Name the property set and property when the answer came from one.
- "Not available" is a correct and expected answer. If the model does not carry the property, the quantity is null, the property set is absent, or the question needs geometry the tools do not give, say that plainly and say what you looked at. Do not estimate, do not substitute a related property without saying so, and never treat a missing value as zero.
- If a query returns no rows, check whether the category name or property name is spelled as the model spells it (ifc_type_counts and ifc_parameters list what exists) before concluding the answer is nothing.
````
