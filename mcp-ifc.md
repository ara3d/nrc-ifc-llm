---
agent_model: "GPT-5.6 Thinking"
prompt_summary: "Survey current MCP servers and tools that can wrap, query, validate, visualize, edit, or otherwise interact with IFC models, then assess gaps and recommend an Ara 3D MCP architecture."
date: "2026-07-24"
---

# MCP Tools That Can Wrap an IFC

As of **July 24, 2026**, there are several real MCP servers that directly expose IFC models. The most significant recent development is that **IfcOpenShell itself now ships an official IFC MCP server**.

## Current IFC MCP landscape

| Rank | Project | What it exposes | Best suited for |
|---:|---|---|---|
| **1** | **IfcOpenShell IfcMCP** | Full headless IFC querying, validation, geometry checks, rendering, and editing | General-purpose IFC automation |
| **2** | **IFClite MCP** | Broad TypeScript/Rust IFC pipeline with querying, visualization, validation, mutation, and export | Web, TypeScript, and high-performance workflows |
| **3** | **Flinker IFC MCP** | Local IFC analysis, reports, creation, browser viewing, and BCF viewpoints | Packaged end-user assistant |
| **4** | **Bonsai MCP / MCP4IFC** | Live interaction with IFC inside Blender/Bonsai | Visual authoring and geometry modification |
| **5** | **smartaec ifcMCP** | Seven focused IFC data-query tools | Simple read-only querying |
| **6** | **Ekkodale IFC-MCP** | Inventory, properties, filters, and aggregations | Quantitative analysis |
| **7** | **openbim-mcp** | IFC-to-That Open fragments and category queries | Web-viewer integration |

## 1. IfcOpenShell IfcMCP

This is currently the strongest general-purpose starting point. It is part of the official IfcOpenShell ecosystem and keeps the loaded model in memory across calls.

Its tools include:

- `ifc_new`, `ifc_load`, `ifc_reset`, `ifc_save`
- `ifc_summary`, `ifc_tree`, `ifc_info`, `ifc_select`
- `ifc_relations`, `ifc_clash`, `ifc_validate`
- `ifc_schedule`, `ifc_cost`
- `ifc_schema`, `ifc_contexts`, `ifc_materials`
- `ifc_plot` for 2D drawings
- `ifc_render` for off-screen 3D images
- `ifc_shape` for procedural geometry
- `ifc_list`, `ifc_docs`, and `ifc_edit`, which dynamically expose the underlying `ifcopenshell.api`
- `ifc_quantify` for writing calculated quantities back into the IFC

This is particularly interesting because it avoids creating hundreds of individual editing tools. Instead, the model can discover the available IfcOpenShell API functions and invoke them through a small number of meta-tools.

Source: [IfcOpenShell IfcMCP documentation](https://docs.ifcopenshell.org/ifcmcp.html)

**Assessment:** Best existing reference architecture for a headless IFC MCP. Its weak point is that many operations depend on the agent correctly understanding IfcOpenShell APIs and selectors.

## 2. IFClite MCP

IFClite is a newer and much broader IFC toolkit written primarily in TypeScript with a Rust/WASM core. Its MCP package claims approximately **70 typed tools** covering querying, validation, mutation, and visualization.

The underlying toolkit includes:

- IFC2x3, IFC4, IFC4x3, and IFC5/IFCX support
- Fluent and SQL querying
- Property mutation with undo
- IDS validation
- Clash detection and BCF generation
- Model comparison and federation
- STEP, GLB, CSV, JSON-LD, Parquet, and IFCX export
- WebGPU visualization
- 2D drawing generation

It can start an MCP server directly against a model using:

```bash
ifc-lite mcp model.ifc
```

Source: [IFClite MCP](https://www.ifclite.com/mcp)

**Assessment:** Potentially the broadest packaged IFC MCP. It is also very new, so geometry correctness, mutation reliability, and API stability should be validated before adopting it as production infrastructure.

## 3. Flinker IFC MCP

Flinker provides an easily installed Node-based MCP server that runs IfcOpenShell inside a local Pyodide environment. It supports:

- Model summaries and counts
- IFC validation and QA
- Property and classification checks
- CSV and other report generation
- Creating new IFC files
- Opening IFC files in a local browser viewer
- Applying BCF and BCFZIP viewpoints
- Handling IFC, IFCXML, and IFCZIP inputs

The installation is unusually straightforward:

```bash
npx -y ifc-mcp
```

Source: [Flinker IFC MCP on GitHub](https://github.com/flinker-app/ifc-mcp)

**Assessment:** Probably the best current end-user experience. It is less of a fixed domain API and more of a controlled environment in which the agent generates Python using IfcOpenShell.

## 4. Bonsai MCP and MCP4IFC

There are several overlapping projects in this family. They connect the MCP server to a running Blender instance with Bonsai and IfcOpenShell.

The latest Show2Instruct version exposes eight relatively broad tools:

- Scene information
- Selected-object information
- IFC property sets
- Viewport screenshots
- IFC project information
- Execute IfcOpenShell code
- Execute Blender Python
- Save the IFC file

Earlier versions exposed more than 50 higher-level tools for walls, doors, roofs, stairs, procedural geometry, scene analysis, and documentation retrieval. The associated MCP4IFC research project combines predefined BIM tools with RAG-assisted dynamic code generation.

Source: [Bonsai MCP on GitHub](https://github.com/Show2Instruct/bonsai-mcp)

**Assessment:** Best option for an agent that must see and visually edit the model. It has a larger security and reliability surface because the agent can execute arbitrary Blender or Python code.

## 5. smartaec ifcMCP

This is a small, readable Python and FastMCP implementation built on IfcOpenShell. It exposes seven tools:

- `get_entities`
- `get_named_property_of_entities`
- `get_entity_properties`
- `get_entity_location`
- `get_entities_in_spatial`
- `get_openings_on_wall`
- `get_space_boundaries`

It is predominantly read-only and focused on answering structured questions about entities, properties, containment, openings, and space boundaries.

Source: [smartaec ifcMCP on GitHub](https://github.com/smartaec/ifcmcp)

**Assessment:** A good minimal example to study or fork. It does not provide the broader filtering, tabular analysis, visualization, or editing capabilities considered for Ara 3D.

## 6. Ekkodale IFC-MCP

This server concentrates on analytical queries and aggregations. Its tools include:

- Listing entity types
- Retrieving entities with attribute filters
- Getting detailed entity information
- Getting property sets and property names
- Filtering entities by property values
- Generating building inventory statistics

It is designed around questions such as total wall area, largest window, element counts, and property-based filtering.

Source: [Ekkodale IFC-MCP on GitHub](https://github.com/ekkodale/IFC-MCP)

**Assessment:** A reasonable example of a more business-oriented query wrapper, but still an early and relatively small project.

## 7. openbim-mcp

Helen Kwok's `openbim-mcp` is based on That Open's fragments and `web-ifc`. It exposes three primary operations:

1. Convert IFC to fragment format.
2. Load a fragment model.
3. Fetch elements by IFC category, with selected attributes and relations.

It is mainly oriented toward efficient web viewing rather than comprehensive IFC analysis or editing.

Source: [openbim-mcp on GitHub](https://github.com/helenkwok/openbim-mcp)

**Assessment:** Useful as an example of wrapping a derived visualization representation rather than repeatedly processing raw IFC.

## Adjacent MCP servers

Two other projects are useful companions but do not directly wrap a loaded IFC model:

- **IFC IDS MCP** creates, edits, and validates buildingSMART IDS requirement files using IfcTester. It would pair naturally with an IFC validation server.  
  Source: [IFC IDS MCP on GitHub](https://github.com/vinnividivicci/ifc-ids-mcp)

- **IFC Core MCP** exposes IFC4.3 schema definitions, inheritance, attributes, and standard property-set documentation. It is a semantic reference server rather than a model server.  
  Source: [IFC Core MCP on GitHub](https://github.com/shuji-bonji/ifc-core-mcp)

Revit MCP servers that merely provide an `export_ifc` tool should also be treated separately: they wrap Revit, not the exported IFC model.

## What is still missing

Across the projects reviewed, most current IFC MCPs are centred on **one locally loaded file** and one of three patterns:

1. Fixed query functions.
2. A generic IFC selector plus generic edit execution.
3. Arbitrary Python execution through IfcOpenShell or Blender.

There is much less support for:

- Persistent immutable element sets
- Federated multi-model queries
- Portfolio-scale IFC collections
- Epochs and model-version tracking
- Reusable query histories
- Tabular pipelines and joins with external databases
- Analytics metadata embedded back into IFC
- Reversible modifier stacks
- Viewer selection, colouring, and viewpoint workflows as first-class operations
- Stable identifiers spanning IFC, Revit, BOS, and lakehouse representations

This conclusion is an inference from the reviewed toolsets rather than an explicit claim made by any one project.

## Recommendation for Ara 3D

For experimentation, test **IfcOpenShell IfcMCP** first. It has the cleanest general-purpose tool decomposition and the strongest underlying IFC implementation.

For an Ara 3D/BOS MCP, avoid exposing the entire IFC API or creating 70–200 individual tools. A stronger core would probably contain around 15 tools:

```text
open_model
close_model
get_model_summary
get_spatial_tree

find_elements
get_elements
get_properties
get_relationships

create_element_set
combine_element_sets
create_data_table
compute_quantities

validate_model
create_view
export_result
```

Then provide discoverable operation registries behind tools such as:

```text
list_available_queries
describe_query
execute_query

list_available_modifiers
describe_modifier
apply_modifier
```

This gives the flexibility of IfcOpenShell's `ifc_list` / `ifc_docs` / `ifc_edit` approach without flooding the agent with hundreds of schemas.

The differentiator would not simply be **“talk to an IFC.”** It would be:

> Persistent, composable IFC/BOS workflows connected to visualization, analytics, and external operational data.
