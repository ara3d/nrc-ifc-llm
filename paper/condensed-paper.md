# Storing, displaying, and querying building analytics on IFC models with a large language model agent layer

**Christopher Diggins**, Ara 3D / Studio 2.5. Prepared for the National Research Council of Canada. Condensed version, 2026-09-19.

## Abstract

Building performance analytics such as embodied carbon, operational carbon, and energy use intensity are computed by tools outside the building information model and delivered as spreadsheets and reports. This paper addresses three connected questions for openBIM workflows built on the Industry Foundation Classes (IFC): where analytics should be stored so that they travel with the model, how they should be displayed on the geometry, and how a large language model (LLM) can be placed in front of an enriched model so that it may be queried in natural language.

Twelve storage mechanisms within IFC 4.3 are compared and a three-layer approach is recommended: scalar summaries in custom property sets, a reference to an external columnar dataset joined on `GlobalId`, and a metric dictionary. For display, colour mapping driven by the same tables in which the analytics are stored is recommended. For querying, the language model is given not the IFC file but a small typed read-only tool surface over the Model Context Protocol (MCP), backed by a columnar copy of the model in DuckDB. A proof of concept on the buildingSMART Duplex Apartment model, 38,898 STEP (Standard for the Exchange of Product model data) entities, enriched the file with 664 property sets and 2,438 typed values written byte-exactly and reversibly, answered eight natural-language questions through the tool surface (seven of eight matching the expected answer in a hand-driven session, four of eight in an unattended run), and evaluated four accessible-door-clearance rules over 14 doors, producing 56 verdicts across all four verdict categories, byte-identical across runs, with rule DC-W1 matching independently derived ground truth door by door. The unattended run exposed one defect in the storage recommendation, namely that storey and building aggregates share the element property names, and that is the first correction to make.

## 1 Introduction

The National Research Council of Canada (NRC) produces analytics on building models: operational carbon, embodied carbon, energy use, and related indicators. These are computed by simulation and life-cycle assessment tools whose inputs may derive from an IFC model but whose outputs are not written back to it. Three activities become difficult once the results have left the model. A designer who opens the model looking for the walls carrying the most embodied carbon will not find them there. A downstream tool cannot locate the results without the original tool and its project file. And a question such as "what is the total operational carbon on Level 2" requires a person who understands both the analysis tool and the model.

The components needed already exist. The IFC schema [1] has several mechanisms for attaching data to elements. The Information Delivery Specification (IDS) [2] can state which results a delivered model must carry. Language models can turn a question into a query. What is absent is a settled practice for combining them, and the obvious combination, handing the IFC file to the language model, does not work at the scale of real models.

The statement of work [20] sets three objectives, and the paper follows them: storage (Section 3), display (Section 4), and querying (Section 5), with the evidence in Section 6, limitations in Section 7, and what to build next in Section 8. The contributions are a ranked comparison of twelve storage mechanisms with a three-layer recommendation, an implemented argument that the language model belongs behind a small typed tool surface over a columnar copy of the model, a byte-exact write-back path, an executed and reproducible demonstration on a public model, and a roadmap for an open bidirectional viewer.

## 2 Background

IFC is an ISO standard schema for building information, ISO 16739-1:2024 [1], most often exchanged as STEP text files: a list of numbered entities, each element carrying a `GlobalId` intended to be stable across exports, placed in a hierarchy of project, site, building, storey, and space. A property set (`IFCPROPERTYSET`) is a named group of typed single-value properties attached to elements through a relationship entity. Standard sets are prefixed `Pset_`; custom sets may be defined by anyone.

Three consequences shape everything that follows. Property names are effectively the schema, so two tools that both write `EmbodiedCarbon` may disagree on units, stage, and method. The file is a text serialisation of an object graph, so reading one fact requires parsing the whole file; the Duplex model has 38,898 entities and larger buildings run to millions. And writing is fragile, because most IFC libraries load the file into their own object model and re-serialise it, changing numbering and formatting throughout, so a client who receives an enriched file cannot easily see what changed.

An IDS file states, for a class of objects (its applicability), what those objects must contain (its requirements), and validators report a pass or fail per element. NRC already maintains an IDS framework, so any property set recommended here should be one an IDS can require. The applicability-plus-requirements shape is also the shape of a code-compliance rule, which Section 6.2 exploits.

Practical systems give a language model tools rather than the file itself: functions with typed arguments and results. MCP [7] is an open standard for describing and calling such tools, so a server written once serves any MCP-capable client.

The proof of concept is built on the open-source BIM Open Toolkit [8], MIT licence. BIM Open Schema (BOS) [9] is a columnar representation of a model, one Parquet table each for entities, parameters, relations, and geometry, loaded directly into DuckDB. BimOpenFlow is a dataflow graph over those tables: nodes are pure functions from tables to tables, a graph is a JSON document, and four operations (`addNode`, `connect`, `setParam`, `removeNode`) back the HTTP API, the MCP tools, and every gesture in the web editor. Nodes that write files run only inside an explicit run, which records the graph hash and every input hash.

## 3 Storage of analytics within IFC

An analytics value is more than a number. To be reusable it needs the element or container it describes, identified by `GlobalId`; the metric; the unit; the lifecycle stage or time basis, such as A1 to A3 or annual; the scenario; and the run that produced it. Each mechanism is judged on how much of this it carries and on portability (does the value travel with the file), queryability (can a tool or language model find it without special knowledge), interoperability (do other IFC tools read it), and scalability (does it still work for thousands of metrics or time series). Table 1 summarises the twelve mechanisms examined in the options brief [21].

**Table 1** Twelve mechanisms within IFC 4.3 for carrying analytics, scored on four properties.

| Mechanism | IFC basis | Portability | Queryability | Interop. | Scalability |
|---|---|---|---|---|---|
| Custom property sets | `IfcPropertySet` | High | High | Med–high | Medium |
| Standard environmental sets | `Pset_EnvironmentalImpactIndicators` | High | High | Medium | Medium |
| Element quantities | `IfcElementQuantity` | High | High | High | Medium |
| Material properties | `IfcMaterialProperties` | High | Medium | Medium | High |
| Spatial aggregates | Property sets on space, storey, building | High | High | Medium | High |
| External dataset reference | `IfcDocumentReference` plus join key | Medium | Very high | Medium | Very high |
| Library and classification refs | `IfcLibraryInformation`, bsDD | Medium | Medium | Med–high | High |
| Performance history | `IfcPerformanceHistory` | Medium | Medium | Low–med | Medium |
| Constraints and metrics | `IfcMetric`, `IfcObjective` | Medium | Medium | Low–med | Medium |
| Custom schema extension | New entity types | Low | Custom only | Low | Medium |

Custom property sets are the simplest and most widely readable, and the external dataset reference is the only one that scales. No single mechanism satisfies all four properties, so three are recommended together.

**Layer 1: summary values in custom property sets.** The scalar values that people inspect, filter by, colour by, and ask about are written into property sets on elements and spatial containers, one set per topic: `Pset_NRCEmbodiedCarbon`, `Pset_NRCOperationalCarbon`, `Pset_NRCEnergyPerformance`, and `Pset_NRCAnalyticsProvenance`. Every set carries `ScenarioName` and `AnalysisRunId`, so a value can never be separated from its run. Units and lifecycle stages are carried in the property names, as in `EmbodiedCarbon_A1A3_kgCO2e`, so the meaning survives tools that drop the IFC unit assignment.

**Layer 2: a reference to the full dataset.** An `IfcDocumentReference` on the project names the external result table, its format, checksum, and join key. The table is long-format, one row per run, element, and metric (`AnalysisRunId, GlobalId, IfcClass, MetricId, MetricName, Value, Unit, LifecycleStage, Scenario, Source, Confidence, ComputationMethod`), so new metrics never require a schema change. Parquet is recommended; CSV is acceptable for small datasets.

**Layer 3: a metric dictionary.** A short versioned list of identifiers such as `NRC.EC.A1A3.TOTAL` and `NRC.EUI.ANNUAL`, to which every Layer 1 property name and Layer 2 `MetricId` is mapped. It gives the query layer one place to resolve "carbon" to a column and gives an IDS one vocabulary to require.

**Writing without disturbing the file.** The toolkit's editing library treats the source as bytes, finds the highest entity identifier and the owner-history entity, and appends new entities: N `IFCPROPERTYSINGLEVALUE` lines, one `IFCPROPERTYSET`, and one `IFCRELDEFINESBYPROPERTIES` per element and set. Each new entity's `GlobalId` is a deterministic hash of a caller-supplied key, so running the writer twice produces the same bytes. An entity-level diff reports exactly which entities were added, and a remove operation strips them again.

**Recommendation.** Write summary analytics into custom property sets on elements, spaces, storeys, buildings, and the project; put units, stage, scenario, run identifier, and provenance in every set; reference the full result table by `IfcDocumentReference`, joined on `GlobalId` and stored as Parquet; publish a metric dictionary; write by byte-exact patch rather than re-serialisation; and express the whole as an IDS. The first, third, and fifth measures are implemented and tested; the fourth is a document; the IDS remains future work.

## 4 Display of analytics on IFC geometry

Three techniques show a number on a building. Colour coding maps each element's value through a gradient for numeric metrics or a palette for categories and verdicts, and is the most immediate view. Text annotation shows the value in a property panel when an element is selected; panels are universal, whereas scene labels are rare in free viewers and clutter quickly. Aggregated views sum by storey, zone, or category and show a table or chart beside the model, and this is the view on which decisions are taken. A working display presents all three.

The display may be driven from the property sets of Layer 1, in which case any viewer that colours by property works but shows only what was written into the file, or from the external table of Layer 2, in which case the viewer joins the table to the geometry on `GlobalId` and colours by any column of any scenario without rewriting the IFC. The toolkit's dataflow graph takes the second approach. A three-node graph loads the instances of a model, reads a value table, and colours the instances by a chosen column through a chosen colour map; instances with no match in the table are drawn grey, so missing data is visible rather than silently zero. Changing the column re-colours the model without touching the file, and an aggregate node grouped by storey feeds a bar chart or table from the same graph.

![Figure 1](figures/figure-5-3d-operational-carbon.png)

_Figure 1 The enriched Duplex model coloured by operational carbon (synthetic values) through a viridis gradient. The graph on the left is the whole description._

![Figure 2](figures/figure-8-3d-dc-w1-verdicts.png)

_Figure 2 Rule DC-W1, requiring a leaf width of at least 850 mm: 8 pass and 6 fail, coloured on the 14 doors. The rule is evaluated by a rule node inside the same graph that colours the model._

When an element is picked, the pane lists its property sets, and the analytics sets appear beside the authoring tool's own sets because they are ordinary property sets in the file. The same path holds on a real building of 456,598 instances, a private sample.

The viewer inventory [23] shortlists Bonsai (Blender), xBIM Xplorer, That Open Components, IFClite, FreeCAD NativeIFC, BIMvision, FZKViewer, and the toolkit's own web viewer. All but FreeCAD (partial) colour by property, and all have a property panel; FZKViewer cannot colour from an external table at all, and the others need a script or plug-in to do it, except the toolkit's, where it is a dataflow join. A seven-step test kit exists, and only the toolkit row has been run through it.

**Recommendation.** Drive colour from a value table joined on `GlobalId`, draw unmatched elements grey, show the selected element's Layer 1 sets in a standard property panel, and provide a per-storey and per-category aggregate beside the model from the same table. For a screenshot-level deliverable, write Layer 1 sets and use any viewer that colours by property; for an interactive deliverable, use the toolkit's graph and viewer. Bonsai should be the reference desktop viewer for verification, because it exposes the full IFC through IfcOpenShell and reproduces the join in a few lines of Python.

## 5 The language model and agent layer

A question such as "what is the total operational carbon on Level 2" requires finding the storey entity, following containment to its elements, following each element's property relationship to its set, reading the value, and summing. In a file of 38,898 entities those entities are scattered, and the file exceeds any model's context window. Even where a file fits, a language model reading STEP text does arithmetic by pattern matching and produces plausible rather than correct totals. The alternative is tools, so that the model reasons over results that are small, structured, and correct. Four design principles were derived from running varied questions against the implementation and reading the transcripts.

- **Few, typed, read-only tools.** A server exposing the whole IFC API as 200 tools gives the model too many ways to be wrong. The implementation exposes 29 tools grouped by question shape. Every SQL tool accepts one read-only statement; `DROP`, `INSERT`, and statement chaining are rejected, and the rejection is tested.
- **A columnar copy rather than the object graph.** The IFC is converted once per session to BOS and loaded into DuckDB. Questions become SQL over tables with text views, companion views that resolve BOS's interned string and enum codes into readable names and values, which a model writes reliably.
- **Questions run in the opposite direction.** Per-element tools ("what does element N carry") are the wrong shape for almost every real question ("which elements are load bearing"). An inverted parameter index answers those in a single call. Without it the model made one call per element.
- **Answers carry their derivation.** Every list result reports its unpaged total, so the model can tell a complete answer from a truncated one. In the dataflow surface a run record pins the graph hash and every input hash, so a number arrives with a means of recomputing it.

The IFC MCP server exposes data tools (entities, attributes, properties, quantities, relations, spatial tree), geometry tools (meshes, bounds, volumes), and analytics tools (convert to BOS, list tables, run read-only SQL, export). In the hand-driven session, a typical answer took one to two calls: a conversion and a SQL statement whose result the model restates with its run identifier.

The second surface is the BimOpenFlow MCP server, whose six tools (`describeDatabase`, `getNodeCatalog`, `editGraph`, `evaluate`, `getResult`, `createRun`) include `editGraph`, which applies the same four operations that back the web editor. A question becomes a graph of small nodes rather than one SQL string, the graph persists where a person can open and edit it, the next question ("now only the doors") is an edit to the same graph, and the graph that colours the model is the same kind of object, so "colour Level 2 by the values just summed" is one further node. Making this work on large models required a schema summary the model can afford to read, a single call to apply a list of edits, and a host-side check that every node evaluated and the answer table has rows. On the toolkit's own test database, twelve requests produced ten correct graphs, one honest answer without a graph, and one correctly empty graph with an explanation; these figures are not a measurement of the carbon-and-energy task.

**Compliance as a query.** A code rule is a query with a verdict column. A `check.rule` node takes a table of element rows and a Boolean expression and appends `verdict`, `checkId`, `checkTitle`, and `citation`. True yields `Pass`; false yields `Fail`, or `NeedsReview` where a second expression says so; a null result, meaning the required fact was absent, yields `InfoNotAvailable`. Absence is reported and never skipped. The verdict table is an ordinary table that may be coloured onto the model, summed per storey, or written back into the IFC.

**Recommendation.** Place the model behind a small typed read-only tool surface; convert the IFC once to columnar form and answer with SQL over text views; provide inverted parameter tools; make every answer carry its derivation; treat compliance checks as queries with a verdict column in which missing data is an explicit verdict; and use MCP so one server serves a chat client, a custom agent, and the web editor alike.

## 6 Proof of concept and results

Both case studies use the buildingSMART Duplex Apartment model [18], IFC2X3, 38,898 entities, two storeys, 14 doors, 61 furnishing elements, with BIM Open Toolkit at commit `71790a7`, .NET 8, and DuckDB. Before either study, automated tests exercise conversion, table listing, paged SQL, read-only enforcement, text views, and export against the FZK-Haus model [19], with the server run as a live subprocess over stdio.

### 6.1 Case study A: natural-language questions over an enriched model

Executed 2026-09-17 with synthetic analytics: each of the 218 physical elements received a type-based embodied carbon value with deterministic jitter, and the test kit's operational carbon and energy intensity columns were reused. The roof deliberately received no embodied-carbon set. A generator produced Layer 1 values plus storey and building aggregates, a Layer 2 table, and a provenance set; a .NET program wrote them with the byte-exact writer; expected answers were computed from the CSV alone, without the IFC or the server. The enrichment added 3,766 entities (664 property sets, 2,438 typed values). The entity diff listed exactly the added entities, removing them restored the source byte for byte, and a second run produced identical bytes.

The eight questions were answered twice: by the author choosing tool calls by hand with every call recorded verbatim, and on 2026-09-18 unattended by `gpt-5`, one fresh conversation per question, 35 tool calls in all (Table 2).

**Table 2** Case study A: expected against returned, hand-driven and unattended.

| # | Question | Expected | Hand-driven | Unattended `gpt-5` |
|---|---|---|---|---|
| Q1 | Total operational carbon, building | 37,196.2 | Match, from the aggregate and the sum of 218 elements | Match |
| Q2 | Higher mean energy intensity, L1 or L2 | Level 2, marginally (40.50 vs 40.56) | **Miss**: Level 1; the relation walk reached 93 of 103 Level 1 elements | Match, via the new `StoreyOfEntity` view |
| Q3 | Five highest operational carbon elements | Two walls, a cabinet, two walls | Match | **Miss**: ranked the building and storeys, which carry the same property |
| Q4 | Carbon of door `M_Single-Flush:0762 x 2032mm` | 54.0, first of four | Match: all four listed, ambiguity stated | Match: all four listed, question returned |
| Q5 | Operational carbon per category | Wall 22,854.1, Floor 5,593.5, ... | Match against the per-class expectation (walls 17,547.4), grouped by IFC class | Partial: by IFC class, container rows not excluded |
| Q6 | Which run, and when | run-2026-09-17-01 | Match, with tool, method, dataset URI | Match |
| Q7 | Embodied carbon of the roof | Not available | Match | **Miss**, and informative: found the roof's `IFCSLAB` member and said so |
| Q8 | Embodied carbon per storey | L1 49,451.2; L2 48,696.8; ... | Match | **Miss**: exactly double each |

Seven of eight matched in the hand-driven session and four of eight unattended. Three of the unattended misses share one cause that matters more for the storage recommendation than for the agent. The Layer 1 aggregates on the storey and building entities carry the same property set and property name as the element values. An agent that ranks everything carrying `OperationalCarbon_kgCO2e_per_year` counts the building and storeys as elements (Q3, Q5), and when it groups elements by storey it adds the storey's own aggregate to its elements' sum and doubles every total (Q8). The hand-driven session avoided this by excluding container classes in each query, which is knowledge a prompt can carry but a file should not require. The aggregate sets should be given their own names, for example `Pset_NRCStoreySummary`.

Q7 is a different lesson: the roof is an assembly whose slab member received values, and the agent found them and said which entity carries them, which is the better answer. The hand-driven Q2 miss traces to assembly parts reached through `MemberOf` rather than `ContainedIn`; a `StoreyOfEntity` view that walks all three relations was added afterwards and the unattended run used it.

### 6.2 Case study B: door clearance, from code text to verdicts

Executed 2026-08-04 and independently re-run 2026-08-05; every claim is backed by a test or commit in the demonstration record [26]. Four provisions modelled on the accessible-door requirements of NBC 2020 [6] were expressed in a JSON rule file, each with an identifier, a citation labelled illustrative, an applicability filter (entity type and optional storey), requirement parameters, and verdict semantics (Table 3).

**Table 3** The four rules and their verdict totals over 14 doors.

| Rule | Requirement | Pass | Fail | N/A | Inconclusive |
|---|---|---|---|---|---|
| DC-W1 | `OverallWidth` of at least 850 mm | 8 | 6 | 0 | 0 |
| DC-W2 | `Pset_DoorCommon.ClearWidth` of at least 850 mm | 0 | 0 | 0 | 14 |
| DC-M1 | Width in type name agrees with `OverallWidth` within 25 mm | 14 | 0 | 0 | 0 |
| DC-Z1 | Manoeuvring zone in front of door free of furnishing; Level 1 only | 4 | 2 | 8 | 0 |

![Figure 3](figures/figure-1-door-clearance-pipeline.svg)

_Figure 3 The three stages of case study B: a code provision, its JSON rule, and the checker's verdict records, with the plan-view zone test of rule DC-Z1._

A small engine evaluates every rule against every door and emits one record per pair, sorted by `GlobalId` then rule identifier so the output does not depend on file order. A threshold rule returns `Inconclusive` where the property is absent. The zone rule composes the door's placement chain into an axis-aligned box and tests each furnishing element's origin against it.

Before the checker was written, a separate agent in a separate commit extracted every door's identifiers, name-encoded and declared dimensions, and storey [27]. All 14 doors carry both attributes, the two agree to the millimetre, and widths are 2 at 1250 mm, 6 at 864 mm, 4 at 762 mm, and 2 at 813 mm, predicting 8 pass and 6 fail for DC-W1. The checker matched door by door. All four verdict categories occur for real reasons: DC-W2 is inconclusive everywhere because the model's authors never wrote `ClearWidth`, and the storey filter marks the 8 Level 2 doors not applicable. DC-Z1 found two Level 1 doors with a furnishing element in the manoeuvring zone, a condition that was not staged.

The evaluation runs twice from scratch in the test suite and the SHA-256 of the verdict CSV is asserted identical; a fresh-process re-run the next day gave the same hash. A failing 762 mm door then receives an `Ara3D_Compliance` set carrying `Verdict`, `OverrideVerdict`, `OverrideReason`, and `ReviewedBy`, appended to a copy of the model. The test asserts that the diff lists exactly the added entities, that removing them restores the source byte for byte, and that the source is never modified.

### 6.3 What the two studies show together

Case study B exercises every part of the recommended architecture except the language model: values read from the file, a rule as data, verdicts keyed by `GlobalId` with evidence, results written back byte-exactly, and reproducibility by hash. Case study A places the language model in front of the same tools. Both were deliberately built on one model, one writer, and one table shape, so that a verdict and a carbon value are the same kind of object: a row keyed by `GlobalId` that may be coloured, summed, asked about, and written back.

## 7 Limitations

**Of the proof of concept.** Both studies use one small public model whose Revit family names encode dimensions, which assisted ground truth; NRC's models will not necessarily do so, and rule DC-M1 will likely need a geometric measurement. Case study A was answered by one hand-driven session and one unattended run of one model; one run is not a measurement of reliability, and repeated runs with other models and the renamed aggregate sets are required before an accuracy figure is quoted. The analytics are synthetic: correct in shape, units, and join key, but not derived from an analysis tool. DC-W1 tests leaf width rather than clear width, the zone rule tests origins rather than meshes, and the citations are illustrative and unreviewed by a code authority.

**Of the storage recommendation.** Custom property sets are a convention, not a standard; two organisations writing `Pset_NRCEmbodiedCarbon` with different stages produce files that look compatible and are not. The metric dictionary and an IDS are the mitigations, and neither is implemented. Aggregates share the element property names, as Section 6.1 showed. Units in property names are robust but redundant with `IfcUnitAssignment`, and an external reference detects substitution but not absence.

**Of the query layer.** The dataflow accuracy figures were obtained on the toolkit's test database, not on carbon questions over an enriched IFC. On questions with no single reading, the models tested chose an interpretation rather than asking; the host's check catches empty answers, not wrong interpretations. The IFC loader targets `net8.0-windows`, so the full proof of concept runs only on Windows, and the host is local, single-user, and unauthenticated.

**Of the display recommendation.** The viewer comparison has one row from the test kit. For the others it rests on documented capabilities, and the toolkit row is the only one whose external-table colouring is a join rather than a script, which favours it by construction.

## 8 Future directions

**Near term.** Rename the storey and building aggregate sets, regenerate, re-enrich, and rerun the unattended questions before quoting any match count. Run the viewer test kit through the shortlist, beginning with Bonsai. Repeat both studies on an NRC model with a real dataset once supplied. Wire the existing volume and bounds tools into the zone rule.

**IDS as the rule format.** The threshold rules DC-W1 and DC-W2 are exactly what IDS was designed for: an applicability (`IFCDOOR`) and a requirement (a property with a minimum). Layer 1 should be expressed as an IDS specification and delivered models validated against it before any query runs, and the threshold rule kind should map to IDS so a rule file carries IDS requirements beside the geometric kinds IDS cannot express.

**Knowledge graphs and world models.** The columnar tables are a graph flattened into edge lists, and converting them to RDF using the Building Topology Ontology [4] is mechanical. The gain is joins outside the building, to product databases, climate zones, and regulation text; the cost is tooling, since a language model writes SQL more reliably than SPARQL at present. The columnar form should remain the working representation with an RDF export published from it. A learned "world model" that predicts embodied carbon from partial geometry needs a ground truth to train and audit against, and the enriched, versioned models this pipeline produces are what that ground truth looks like.

**Federated collections.** Every IFC MCP server surveyed [24] operates on one loaded file. A portfolio needs element sets that persist across sessions, queries spanning models, and identifiers that survive Revit to IFC to BOS. A longer-horizon vision [28] treats a project as a repository with checkpoints, options as branches, and decisions linked to evidence.

**A bidirectional viewer.** The toolkit's WebGL viewer knows nothing of IFC; the graph feeds it instance tables with colour columns, and the byte-exact writer returns property sets to the file. What is absent is the set of operations that would let an agent drive the viewer: `select` and `get_selection`, `color_by`, `isolate`, `hide`, `section`, `set_viewpoint` and `get_viewpoint` exportable as BCF [3], `annotate`, `snapshot` with the graph hash that produced it, and `write_psets`. Each is a graph node as well as a tool. Four stages follow: the viewer as a graph sink (largely complete); selection as data; write-back from the viewer, with the entity diff shown before it is applied; and multiple models with history. Throughout, every file write goes through the byte-exact path inside a run, and one set of operations serves the mouse, the HTTP API, and the agent.

## 9 Conclusion

Summaries belong in the file and the full data beside it. Custom property sets carry the scalar values people inspect, with units, stage, scenario, and run identifier in every set, and an `IfcDocumentReference` points to a long-format Parquet table for everything else, tied together by a metric dictionary. Writing is a byte-exact patch, so an enriched file differs from the original only in what was added, and the additions can be removed to recover the original exactly. The one correction required is that aggregate sets be given names of their own.

Display should be driven from tables rather than from the file: one value table joined on `GlobalId` drives colour, selection detail, and per-storey aggregates from a single description, with unmatched elements grey.

The language model belongs behind tools. A small typed read-only surface over a columnar copy of the model lets it write queries that are correct, checkable, and inexpensive, with every answer carrying its derivation. Compliance rules are queries with a verdict column, and missing data is a verdict rather than a silent pass.

What the client gains is not a viewer and not a checker but a shape for the data: a row keyed by `GlobalId` that may be a carbon value, a verdict, or an override, and that may be coloured, summed, asked about, validated by an IDS, and written back. Everything proposed for the future builds on that shape rather than replacing it.

## References

Numbering follows the full paper so that the two may be read side by side.

[1] ISO 16739-1:2024. Industry Foundation Classes (IFC). https://ifc43-docs.standards.buildingsmart.org/
[2] buildingSMART. Information Delivery Specification (IDS) 1.0, June 2024.
[3] buildingSMART. BIM Collaboration Format (BCF).
[4] Rasmussen, M. H., et al. BOT: The Building Topology Ontology. Semantic Web 12(1), 2021.
[6] National Research Council of Canada. National Building Code of Canada 2020.
[7] Model Context Protocol specification. https://modelcontextprotocol.io/
[8] Ara 3D. BIM Open Toolkit, MIT licence. https://github.com/ara3d/bim-open-toolkit (commit `71790a7`).
[9] Ara 3D. BIM Open Schema. https://github.com/ara3d/bim-open-schema
[18] buildingSMART. Duplex Apartment sample model, IFC2X3.
[19] Karlsruhe Institute of Technology. FZK-Haus reference model, `AC20-FZK-Haus.ifc`. https://www.ifcwiki.org/index.php/KIT_IFC_Examples
[20] Statement of Work, `statement-of-work.md`, this repository.
[21] Storing analytics in IFC: options brief, `storing-analytics-in-ifc.md`, this repository.
[23] IFC viewer inventory and test kit, `ifc-viewers.md` and `IFC-Test-Kit/README.md`, this repository.
[24] MCP tools that can wrap an IFC, `mcp-ifc.md`, this repository.
[26] Door clearance demonstration, `door-clearance-demo.md`, this repository.
[27] Door ground-truth dataset, `IFC-Test-Kit/door_ground_truth.md`, this repository.
[28] AI-assisted architecture planning and design on Git, `ai_assisted_architecture_design_system.md`, this repository.
