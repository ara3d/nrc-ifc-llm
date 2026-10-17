# Annex C: Tool surface of the IFC MCP server

This annex lists the tools of the `bimopen-ifc` MCP server (Model Context Protocol, the protocol through which a language model calls tools) that answers questions about IFC files, 37 in all, with one line each. Source: `deps/bim-open-data/src/mcp/BimOpenMcp.Ifc/README.md`, from the development clone of the BIM Open Toolkit, `bim-open-toolkit` at commit 6f37755, the content of the coming tag `v0.2`. Every analytics value in this annex is synthetic: the proof of concept generates it, and it does not describe a real building.

The proof-of-concept record `poc/results/tools-list.json` lists the 29 tools the server offered on 2026-09-18; the tools below that it lacks (the IDS checks, `frag_to_bos`, and the `bos_*` tools) were added since. The unattended runs of the paper's questions use the toolkit's `bimopenmcp-ifc-ask` runner, which hides four tools from the model: the two that write files, `ifc_export_glb` and `ifc_sql_export` (marked "file-writing" below), and the two session tools `ifc_close` and `ifc_models` (marked "hidden"), which matter only to a client holding several models open. Every `ifc_*` tool takes the model's absolute path as `path`.

## Open and inspect

| Tool | Answers |
|---|---|
| `ifc_open` | Schema and entity count. Optional — any tool opens the file it is given. |
| `ifc_close` | Frees a model held open. **(hidden from the unattended runs)** |
| `ifc_models` | Lists the models held open. **(hidden from the unattended runs)** |
| `ifc_header` | STEP header: description, originating file name, schema. |
| `ifc_type_counts` | Entity counts by IFC type, most common first. |
| `ifc_search` | Entities whose name, GlobalId, or type contains some text. |
| `ifc_entity` | One entity by STEP id, with its raw attributes. |
| `ifc_entities_of_type` | Every entity of one type. |
| `ifc_attributes` | Raw STEP attributes by position. |
| `ifc_properties` | Properties grouped by property set. |
| `ifc_quantities` | Lengths, areas, volumes, counts, weights, times. |
| `ifc_property_sets` | Set names and sizes, without values. |
| `ifc_parameters` | Every parameter in the model with element counts, ranges, and sample values. |
| `ifc_parameter_values` | The distinct values of one parameter and how many elements hold each. |
| `ifc_find_by_parameter` | Elements whose parameter passes a test (`eq`, `contains`, `gt`, …). |
| `ifc_parameter_table` | A row per element, a column per parameter. |
| `ifc_relations` | Relationship edges touching an entity. |
| `ifc_spatial_tree` | Project → site → building → storey → space. |
| `ifc_spatial_contents` | Elements directly inside one container. |
| `ifc_element_containment` | The container chain above an element. |
| `ifc_ids_specifications` | The specifications of an IDS file, with no model: what each selects, what it requires, and whether every facet is supported. |
| `ifc_ids_check` | Checks a model or a `.bos` file against an IDS (`Ara3D.Ids`): a summary per specification, the loader's and evaluator's warnings, and a page of verdict rows, filterable by `verdict`. |

## Tables and SQL

| Tool | Answers |
|---|---|
| `ifc_to_bos` | Converts a model to BIM Open Schema, optionally saving the `.bos` file. |
| `ifc_table` | The tables and views a query can use, with row counts and column types. Takes an IFC or a `.bos` path. |
| `ifc_sql` | A read-only DuckDB query over the converted model or a `.bos` file, paged. |
| `ifc_sql_export` | The full result of a query, written to `.csv`, `.parquet`, or `.json`. Takes an IFC or a `.bos` path. **(file-writing; hidden from the unattended runs)** |
| `bos_table` | `ifc_table` with the path argument named `bosPath`. |
| `bos_sql` | `ifc_sql` with the path argument named `bosPath`. |
| `frag_to_bos` | Converts a That Open Fragments 2 file (`.frag`) to BOS, with a DuckDB database beside it, and keeps the model open for the `bos_*` tools. |

## Geometry

| Tool | Answers |
|---|---|
| `ifc_mesh` | Mesh statistics for an element or the whole model. |
| `ifc_bounds` | Bounding boxes, per element and whole-model. |
| `ifc_volume` | Volume and surface area from geometry. |
| `ifc_meshing_diagnostics` | What failed to mesh, and why. |

## Export

| Tool | Answers |
|---|---|
| `ifc_export_glb` | Writes a GLB from the model's BOS conversion (web-ifc geometry), or from a `.bos` file: one node per instance with its own material, stepId, globalId and entityIndex in each node's extras; hidden instances only when named in `ids`. **(file-writing; hidden from the unattended runs)** |
| `bos_export_glb` | Writes a `.bos` model's geometry as GLB, entity index and GlobalId in each node's extras; hidden instances only when named in `entityIndices`. |
| `bos_export_usd` | Writes a `.bos` model as an OpenUSD `.usda` stage with element data as `bim:` attributes. |
| `bos_export_bcf` | Writes the rows of a SQL query over a `.bos` model as BCF 3.0 topics, one per `Title`. |

`bos_export_glb`, `bos_export_usd`, and `bos_export_bcf` also write files; they were added after the runs and are not in the recorded 29.
