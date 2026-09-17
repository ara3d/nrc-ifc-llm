# 2. Background

This section gives the minimum needed to follow the rest of the paper. Readers familiar with
IFC, IDS, and MCP can skip to Section 3.

## 2.1 IFC and its property mechanisms

IFC is an ISO standard (ISO 16739) schema for building information, most often exchanged as
STEP Physical Files (`.ifc`). A file is a list of numbered entities. Each building element is an
entity such as `IFCDOOR` or `IFCWALL`, with a `GlobalId` that is meant to be stable across
exports and tools. Elements are placed in a spatial hierarchy of project, site, building,
storey, and space through `IFCRELCONTAINEDINSPATIALSTRUCTURE`.

IFC has several ways to attach data to an element, and Section 3 compares them. The one that
matters most for this paper is the property set. A property set (`IFCPROPERTYSET`) is a named
group of properties; a single-value property (`IFCPROPERTYSINGLEVALUE`) carries a name, a typed
value, and an optional unit; and a relationship (`IFCRELDEFINESBYPROPERTIES`) attaches the set
to one or more elements. Standard sets are prefixed `Pset_`; anyone may define custom sets.

Three consequences shape everything that follows.

- **Property names are the schema.** Two tools that both write `EmbodiedCarbon` as a property
  can still disagree on units, lifecycle stage, and method. Portability of the file does not
  give portability of the meaning.
- **The file is a text serialisation of an object graph.** Reading any one fact requires
  parsing the whole file. The Duplex Apartment model used in this paper has 38,898 entities;
  larger buildings run to millions.
- **Writing is fragile.** Most IFC libraries load the file into their own object model and
  re-serialise it, which changes entity numbering, formatting, and sometimes content. A client
  who receives an "enriched" file that differs everywhere from the one they sent has no easy
  way to check what changed.

## 2.2 Information Delivery Specification

IDS is a buildingSMART standard (IDS 1.0, June 2024) for machine-readable information
requirements. An IDS file states, for a class of objects (its applicability), what those
objects must contain (its requirements): a property with a certain name and permitted values,
a classification, a material, an attribute. Validators check an IFC file against an IDS and
report pass or fail per element.

For this project IDS matters in two ways. NRC already has an IDS framework, so any property
set the paper recommends should be one an IDS can require. And the applicability-plus-
requirements shape of an IDS specification is the same shape as a code-compliance rule, which
Section 6 uses. The repository document [ids.md](../ids.md) gives a longer introduction.

## 2.3 Linked data and IFC-LBD

The Linked Building Data community expresses building information as RDF graphs, using
ontologies such as BOT (Building Topology Ontology) and mappings from IFC (IFC-LBD, ifcOWL).
This representation is well suited to joining building data with other graphs and to
reasoning. It is included in the storage comparison in Section 3 and treated as a future
extension in Section 8, because the client's current workflow is file-based and the tooling for
LBD is less mature than that for IFC files and columnar tables.

## 2.4 Large language models as query interfaces

An LLM can turn a natural-language question into a structured query, but it has no reliable way
to read a 40,000-entity STEP file. Practical systems give the model tools: functions it may
call, with typed arguments and results, that do the reading. The Model Context Protocol (MCP)
is an open standard for describing such tools and calling them over a stream, so that any
MCP-capable client (Claude Code, other chat clients, or a custom agent) can use a server
written once.

The repository document [mcp-ifc.md](../mcp-ifc.md) surveys seven IFC MCP servers that existed
in mid-2026. They fall into three patterns: fixed query functions over one loaded file; a
generic selector plus generic edit operation; and arbitrary Python execution through IfcOpenShell
or Blender. None of them provided persistent element sets, joins with external tables, or
analytics written back into the file. Section 5 describes the design chosen here in that light.

## 2.5 BIM Open Schema and the toolkit used

The proof of concept is built on the open-source BIM Open Toolkit (MIT licence). Two parts of
it are used.

**BIM Open Schema (BOS)** is a columnar representation of a building model: one table each for
entities, parameters, relations, and geometry, with strings and numbers pooled. Parameters are
stored entity-attribute-value, one table per primitive type. Relations use a closed vocabulary
(`PartOf`, `ContainedIn`, `HostedBy`, `BoundedBy`) that covers both IFC and the Revit API. A
`.bos` file is a zip of Parquet tables and loads directly into DuckDB. A converter turns an IFC
file into BOS in one pass.

**BimOpenFlow** is a dataflow graph over those tables. Nodes are small pure functions from
tables to tables; a graph is a JSON document; and four operations (`addNode`, `connect`,
`setParam`, `removeNode`) back the HTTP API, the MCP tools, and every gesture in the web
editor. Nodes that write files, including the one that writes property sets into IFC, run only
inside an explicit run, and each run records the graph hash and every input by content hash.

The toolkit also contains a byte-exact IFC editing library, `Ara3D.Ifc.Editing`, which locates
entities by byte range in the source file and writes additions as an appended patch, so that
every byte the writer did not touch is preserved. This is the basis of the write-back path in
Sections 3.5 and 6.3.
