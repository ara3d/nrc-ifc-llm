# 1 Background information

The National Research Council of Canada (NRC) produces analytics on building models: operational carbon, embodied carbon, energy use, and related performance indicators. These are computed by simulation and life-cycle assessment tools whose inputs may be derived from an IFC model but whose outputs are not written back to it. The numbers reside in the tools' own databases, in CSV exports, and in PDF reports.

Three activities become difficult once the results have left the model. The results cannot readily be shown, because a designer who opens the model and looks for the walls carrying the most embodied carbon will not find them there. The results cannot readily be reused, because a downstream tool, or a later project phase, is unable to locate them without the original tool and its project file, and there is no standard place to look. And the results cannot readily be interrogated, because a question such as "what is the total operational carbon on Level 2" or "which doors fail the clearance rule" requires a person who understands both the analysis tool and the model.

Mechanisms that could hold these results are already present in the IFC schema [1]. The Information Delivery Specification (IDS) [2] can state which results a delivered model is required to carry. Large language models can turn a question into a query. None of these components is new. What is absent is a settled practice for combining them, and the obvious combination, in which the language model is handed the IFC file directly, does not work at the scale of real models, for the reasons given in Section 7.1.

The statement of work [20] sets three objectives and a publication, and the work reported here is organised around them. The storage objective asks which IFC mechanisms should carry analytics, at component, zone, storey, and building level, so that the data is portable, reusable, and queryable; it is addressed in Section 5. The display objective asks how analytics should be shown on IFC geometry, and which freely available viewers and libraries support this; it is addressed in Section 6. The query objective asks how an LLM-based layer should be built so that it answers natural-language questions about an enriched model correctly, and so that its answers may be checked; it is addressed in Section 7. The evidence for all three is reported in Section 8.

Five contributions are offered. The first is a comparison of twelve storage mechanisms available within IFC 4.3, ranked on portability, queryability, interoperability, and scalability, with a three-layer recommendation and concrete property-set definitions (Section 5, Annex A). The second is an argument, supported by an implementation, that the language model should be placed behind a small typed read-only tool surface over a columnar copy of the model rather than reading the IFC file, together with a description of that surface (Section 7, Annex C). The third is a byte-exact write-back path for property sets, by which analytics, verdicts, and human overrides may be added to a client's IFC file without altering any byte the writer did not intend to change (Sections 5.5 and 8.3). The fourth is an executed and reproducible demonstration on a public model, comprising a machine-readable provision file, a checker, four verdict categories, independently derived ground truth, hash-verified determinism, and a reversible override recorded in the IFC (Section 8). The fifth is a roadmap for an open bidirectional viewer in which selection, colouring, viewpoints, and write-back are operations an agent may call (Section 11).

# 2 Scope

This report covers the storage, display, and querying of previously computed analytics on IFC models, and the design of an agent layer that answers natural-language questions about such models. It reports two executed case studies on one public model and states what those studies establish and what they do not.

The following are not in the scope of this report. Geometry authoring is excluded. The computation of the analytics themselves is excluded; the report is concerned with what happens to a result after an analysis tool has produced it. The proof of concept is a minimal one and is neither a production viewer, nor a certified compliance checker, nor a replacement for the client's analysis tools. The models used are public samples, and the analytics of case study A are synthetic; NRC's own models and analytics datasets, once supplied, are expected to be used to repeat the runs reported in Section 8. The rule file of case study B expresses provisions modelled on the National Building Code of Canada 2020 [6], but its citations are illustrative paraphrases rather than legal text, and no statement in this report should be read as a determination of code compliance.

# 3 Who should use this report

This report is intended for building performance analysts, BIM managers, building envelope and energy consultants, and software developers working on openBIM tooling, as well as for researchers and for the NRC staff responsible for the Information Delivery Specification framework. The reader is assumed to be familiar with building information modelling in general terms, and with the idea of exchanging models as files, but not with the internal structure of IFC, with IDS, or with the Model Context Protocol. Section 4 defines the terms used throughout, and Section 4.2 gives the minimum technical background needed to follow Sections 5 to 8.

Readers who require only the recommendations should read Sections 5.6, 6.4, and 7.6, each of which states its section's recommendation as a short numbered list. Readers concerned with the evidence should read Section 8 together with Annex D, which records what the executed run did not cover. Readers concerned with what should be built next should read Sections 10 and 11.

# 4 Definitions and abbreviations

## Definitions

**Table 1** Definitions used in this report.

| Term | Definition |
|---|---|
| Analytics value | A number describing an element or a spatial container, produced by an analysis tool, together with the metric, unit, lifecycle stage, scenario, and run that give it meaning. |
| Byte-exact write | An addition to an IFC file performed by appending entities to the original bytes, such that every byte the writer did not intend to change is preserved. |
| Enriched model | An IFC file into which analytics values have been written as property sets. |
| Lifecycle stage | The stage of the building lifecycle to which an environmental result applies, expressed in the notation of EN 15978:2011 [5], for example A1 to A3. |
| Metric dictionary | A versioned list of metric identifiers that fixes the name, unit, and lifecycle basis of each metric, and to which property names and dataset columns are mapped. |
| Property set | A named group of properties attached to one or more IFC objects through a relationship, the mechanism described in Section 4.2. |
| Provenance | The record of which run, tool, method, person, and date produced a value. |
| Run record | An immutable record of one evaluation of a dataflow graph, pinning the graph hash and every input by content hash. |
| Tool surface | The set of typed functions a language model is permitted to call, together with their signatures and their results. |
| Verdict | The outcome of evaluating one rule against one element, taking one of four values as defined in Section 7.5. |

## Abbreviations

**Table 2** Abbreviations used in this report.

| Abbreviation | Expansion |
|---|---|
| AABB | Axis-aligned bounding box |
| BCF | BIM Collaboration Format |
| BIM | Building information modelling |
| BOS | BIM Open Schema |
| BOT | Building Topology Ontology |
| CSV | Comma-separated values |
| EUI | Energy use intensity |
| IDS | Information Delivery Specification |
| IFC | Industry Foundation Classes |
| LBD | Linked Building Data |
| LCA | Life-cycle assessment |
| LLM | Large language model |
| MCP | Model Context Protocol |
| NBC | National Building Code of Canada |
| NRC | National Research Council of Canada |
| RDF | Resource Description Framework |
| SPARQL | SPARQL Protocol and RDF Query Language |
| SQL | Structured Query Language |
| STEP | Standard for the Exchange of Product model data |

## 4.2 Technical background

This subsection gives the minimum needed to follow the remainder of the report. Readers already familiar with IFC, IDS, and MCP may proceed to Section 5.

**IFC and its property mechanisms.** IFC is an ISO standard schema for building information, ISO 16739-1:2024 [1], most often exchanged as STEP Physical Files with the extension `.ifc`. A file is a list of numbered entities. Each building element is an entity such as `IFCDOOR` or `IFCWALL`, carrying a `GlobalId` that is intended to be stable across exports and tools, and elements are placed in a spatial hierarchy of project, site, building, storey, and space through `IFCRELCONTAINEDINSPATIALSTRUCTURE`. Several mechanisms exist for attaching data to an element, and Section 5.2 compares them; the one that matters most here is the property set. A property set (`IFCPROPERTYSET`) is a named group of properties, a single-value property (`IFCPROPERTYSINGLEVALUE`) carries a name, a typed value, and an optional unit, and a relationship (`IFCRELDEFINESBYPROPERTIES`) attaches the set to one or more elements. Standard sets are prefixed `Pset_`, and custom sets may be defined by anyone.

Three consequences of this arrangement shape everything that follows. The first is that property names are effectively the schema: two tools that both write a property named `EmbodiedCarbon` may nonetheless disagree on units, lifecycle stage, and method, so that portability of the file does not confer portability of the meaning. The second is that the file is a text serialisation of an object graph, so that reading any single fact requires parsing the whole file; the Duplex Apartment model used in this report contains 38,898 entities, and larger buildings run to millions. The third is that writing is fragile, because most IFC libraries load the file into their own object model and re-serialise it, which changes entity numbering, formatting, and on occasion content, leaving a client who receives an enriched file that differs everywhere from the one they sent with no straightforward way to establish what changed.

**Information Delivery Specification.** IDS is a buildingSMART standard, IDS 1.0 of June 2024 [2], for machine-readable information requirements. An IDS file states, for a class of objects termed its applicability, what those objects are required to contain, termed its requirements: a property with a certain name and permitted values, a classification, a material, or an attribute. Validators check an IFC file against an IDS and report a pass or a fail for each element. IDS is relevant to this work in two respects. NRC already maintains an IDS framework, so any property set recommended here should be one that an IDS is able to require. Further, the applicability-plus-requirements shape of an IDS specification is the same shape as a code-compliance rule, a correspondence that Section 8.3 exploits. A longer introduction to IDS is given in the repository [22].

**Linked data and IFC-LBD.** The Linked Building Data community expresses building information as RDF graphs, using ontologies such as the Building Topology Ontology (BOT) [4] and mappings from IFC. This representation is well suited to joining building data with other graphs and to reasoning over the result. It is included in the storage comparison of Section 5.2 and treated as a future extension in Section 10.3, because the client's current workflow is file-based and the tooling for Linked Building Data is less mature than that available for IFC files and columnar tables.

**Large language models as query interfaces.** A language model is able to turn a natural-language question into a structured query, but it has no reliable means of reading a 40,000-entity STEP file. Practical systems therefore give the model tools, that is, functions it may call, with typed arguments and results, which perform the reading. The Model Context Protocol (MCP) [7] is an open standard for describing such tools and calling them over a stream, so that any MCP-capable client may use a server written once. A survey of seven IFC MCP servers extant in mid-2026 [24] found three patterns: fixed query functions over one loaded file; a generic selector combined with a generic edit operation; and arbitrary Python execution through IfcOpenShell [10] or Blender. None of the seven provided persistent element sets, joins with external tables, or analytics written back into the file, and Section 7 describes the design adopted here in that light.

**BIM Open Schema and the toolkit used.** The proof of concept is built on the open-source BIM Open Toolkit [8], released under the MIT licence, of which two parts are used. BIM Open Schema (BOS) [9] is a columnar representation of a building model, with one table each for entities, parameters, relations, and geometry, and with strings and numbers pooled; parameters are stored entity-attribute-value, one table per primitive type, and relations use a closed vocabulary (`PartOf`, `ContainedIn`, `HostedBy`, `BoundedBy`) that covers both IFC and the Revit API. A `.bos` file is a zip archive of Parquet [17] tables and loads directly into DuckDB [16], and a converter turns an IFC file into BOS in a single pass. BimOpenFlow is a dataflow graph over those tables, in which nodes are small pure functions from tables to tables, a graph is a JSON document, and four operations (`addNode`, `connect`, `setParam`, `removeNode`) back the HTTP API, the MCP tools, and every gesture in the web editor; nodes that write files, including the node that writes property sets into IFC, run only inside an explicit run, and each run records the graph hash and every input by content hash.

The toolkit further contains a byte-exact IFC editing library, `Ara3D.Ifc.Editing` [29], which locates entities by byte range in the source file and writes additions as an appended patch, so that every byte the writer did not touch is preserved. This library is the basis of the write-back path described in Sections 5.5 and 8.3.
