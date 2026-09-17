# Appendix C. MCP tool surface

The tools the language model is given in Section 5. Two servers are described. Both are in the
BIM Open Toolkit at commit `71790a7`.

## C.1 IFC MCP server (`Ara3D.Ifc.Mcp`)

Answers questions about one or more IFC files. Runs over stdio by default, which is how MCP
clients launch a server, or over HTTP for manual testing. Recent models are kept open in a
session cache (three by default). Every list result takes `skip` and `take` and reports the
unpaged `total`.

**Model and header**

| Tool | Answers |
|---|---|
| `ifc_open`, `ifc_close`, `ifc_models` | Schema and entity count; free a model; list open models |
| `ifc_header` | STEP header: description, originating file, schema |
| `ifc_type_counts` | Entity counts by IFC type |

**Entities and attributes**

| Tool | Answers |
|---|---|
| `ifc_search` | Entities whose name, `GlobalId`, or type contains text |
| `ifc_entity` | One entity by STEP id with raw attributes |
| `ifc_entities_of_type` | Every entity of one type |
| `ifc_attributes` | Raw STEP attributes by position |

**Properties and quantities**

| Tool | Answers |
|---|---|
| `ifc_properties` | Properties grouped by property set |
| `ifc_quantities` | Lengths, areas, volumes, counts, weights |
| `ifc_property_sets` | Set names and sizes |
| `ifc_parameters` | Every parameter in the model with element counts, ranges, samples |
| `ifc_parameter_values` | Distinct values of one parameter and their counts |
| `ifc_find_by_parameter` | Elements whose parameter passes a test (`eq`, `contains`, `gt`, ...) |
| `ifc_parameter_table` | A row per element, a column per parameter |

**Relations and spatial structure**

| Tool | Answers |
|---|---|
| `ifc_relations` | Relationship edges touching an entity |
| `ifc_spatial_tree` | Project, site, building, storey, space |
| `ifc_spatial_contents` | Elements directly inside one container |
| `ifc_element_containment` | The container chain above an element |

**Geometry**

| Tool | Answers |
|---|---|
| `ifc_mesh` | Mesh statistics |
| `ifc_bounds` | Bounding boxes |
| `ifc_volume` | Volume and surface area |
| `ifc_export_glb` | Writes a GLB |
| `ifc_meshing_diagnostics` | What failed to mesh and why |

**Analytics**

| Tool | Answers |
|---|---|
| `ifc_to_bos` | Converts to BIM Open Schema, optionally saving the `.bos` |
| `ifc_table` | Tables and views with row counts and column types |
| `ifc_sql` | One read-only DuckDB statement, paged |
| `ifc_sql_export` | Full result to `.csv`, `.parquet`, or `.json` |

The SQL tools reject anything but a single read-only statement. The text views `EntityText`,
`ParameterText`, and `RelationText` resolve BOS's interned string and enum indexes so that a
query can see names and values.

## C.2 Dataflow MCP server (`BimOpenFlow.Mcp`)

Exposes the graph-editing operations. Each tool is one of the operations behind the HTTP API
and the web editor, so a graph an agent builds is the kind a person builds.

| Tool | What it does |
|---|---|
| `listDatabases` | DuckDB files under the model roots |
| `describeDatabase` | Tables with row counts and columns; with `table`, column types, null and distinct counts, samples, ranges |
| `getNodeCatalog` | Every node kind with ports, parameters, enum values, and capability |
| `listAnalyses`, `getAnalysis`, `saveAnalysis` | The graph library |
| `editGraph` | A list of `addNode`, `setParam`, `connect`, `removeNode` edits, validated together and saved once |
| `addNode`, `setParam`, `connect`, `removeNode` | Single edits |
| `evaluate` | Per-node status: `Ok`, `Unready`, `EffectPending`, `Unavailable`, `Error` |
| `getResult` | One node output as a paged table slice |
| `createRun`, `listRuns` | Freeze an evaluation as an immutable run record; list the archive |

## C.3 Client configuration

Registering the IFC server with an MCP client:

```json
{
  "mcpServers": {
    "ara3d-ifc": {
      "command": "dotnet",
      "args": ["run", "--project", "src/Ara3D.Ifc.Mcp"]
    }
  }
}
```

Under stdio, standard output is the protocol stream and all diagnostics go to standard error.
