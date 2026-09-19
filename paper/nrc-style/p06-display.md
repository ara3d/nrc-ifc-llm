# 6 Display of analytics on IFC geometry

This section addresses the second objective of the statement of work, namely how analytics should be shown on IFC geometry and what freely available software supports this. The viewer inventory [23] lists the candidates, and this section selects among them.

It should be noted that every figure in this section was captured on 2026-09-18 by the toolkit's walkthrough script, `scripts/nrc-walkthrough.mjs` at toolkit commit `66df499`, from the seeded graphs in `samples/nrc-analyses`; the captures and their captions are indexed in the walkthrough index of the repository. The 3D views load because the toolkit's IFC-to-BOS converter now drops a non-finite instance transform, at toolkit commit `53a69d9`, and the web loader hides such an instance instead of rejecting the model, at commit `53129a8`; the failure that preceded these corrections is recorded in Annex D.2 and shown in Figure 14. The comparison in Section 6.3 has one row filled, that of the toolkit's own viewer; the other viewers have not been run through the test kit.

## 6.1 Three ways of showing a number on a building

**Colour coding.** Each element is coloured according to a value. Numeric values map through a gradient, as from low to high embodied carbon, and categorical values map to a palette, as for analysis category or for pass and fail. This is the most immediate view and the one that every stakeholder understands.

**Text annotation.** The value is shown as text, in a property panel when an element is selected, as a label in the 3D scene, or as a tooltip. Property panels are universal, whereas scene labels are rare in free viewers and become cluttered quickly.

**Aggregated views.** Values are summed or averaged by storey, zone, or category and shown as a table or chart beside the model, or as a colouring of the containers themselves, as when storey slabs are coloured by total carbon. This is the view on which decisions are taken: which floor, which system, which option.

Overall, the three techniques are not alternatives to one another. A working display presents all three: the model coloured by metric, the selected element's values in a panel, and a per-storey table alongside.

## 6.2 Sources of the displayed values

Section 5 stored values in property sets (Layer 1) and in an external table (Layer 2), and the display may be driven from either. Where the display is driven from property sets, any viewer able to colour by property works without additional software, which is the path for a screenshot-level demonstration and for handing a file to a recipient who has their own viewer; its limitation is that it shows only what was written into the file. Where the display is driven from the external table, the viewer, or a script in front of it, joins the table to the geometry on `GlobalId` and colours by any column, which shows any metric and any scenario without rewriting the IFC; this requires a viewer with a scripting or data-binding interface.

The toolkit's dataflow graph takes the second approach. A three-node graph loads the instances of a model, aggregates or joins a value table, and colours the instances:

```json
{
  "nodes": [
    { "id": "inst",    "kind": "view3d.instances" },
    { "id": "values",  "kind": "csv.read" },
    { "id": "colored", "kind": "view3d.color" }
  ],
  "edges": [
    { "from": "inst.instances",  "to": "colored.instances" },
    { "from": "values.table",    "to": "colored.values" }
  ],
  "values": {
    "inst":    { "path": "{DATA}/duplex.ifc" },
    "values":  { "path": "{DATA}/analytics_dataset_with_levels.csv" },
    "colored": { "joinColumn": "GlobalId", "valueColumn": "operational_carbon", "colorMap": "viridis" }
  }
}
```

The `view3d.color` node maps a numeric column through a gradient normalised over its range, or a text column through a categorical palette with indices assigned by sorted distinct value, so that colours remain stable when rows are reordered. Instances with no match in the value table are drawn grey, which renders missing data visible rather than silently zero. Changing `valueColumn` to `energy_intensity`, or `colorMap` to `redgreen`, re-colours the model without touching the file.

Aggregated views are produced by the same graph: a `table.aggregate` node grouped by `Level` feeds a `chart.bar` or a `view.table` node, and the same aggregate is able to feed a second `view3d.color` that colours storeys. Figures 1 and 2 show the storey aggregates from the proof of concept as a bar chart and as a table, both from a two-node graph, and Figure 3 shows the property values that were written into the model, as a table.

![Figure 1](../figures/figure-2-storey-carbon-chart.png)

_Figure 1 The storey aggregates of the synthetic dataset, drawn by a `chart.bar` node fed from the storey CSV. The graph on the left is the whole description; the chart is its live output._

![Figure 2](../figures/figure-3-storey-carbon-table.png)

_Figure 2 The same node's output in the Table tab. Building, storey, and roof values are those written into the corresponding IFC entities._

![Figure 3](../figures/figure-4-property-values-table.png)

_Figure 3 The rows given to the byte-exact writer: entity identifier, set name, property name, IFC value type, and value. Each row became one `IFCPROPERTYSINGLEVALUE`._

The 3D colourings of the Duplex model by these values are shown in Figures 4 to 6. Each is produced by a three-node graph comprising `view3d.instances` over the enriched IFC, `csv.read` over the elements table, and `view3d.color` joining them on `GlobalId`. Of the 218 analysed elements, 216 have a mesh in the converted geometry and are coloured; openings and spaces have no row in the table and are drawn grey.

![Figure 4](../figures/figure-5-3d-operational-carbon.png)

_Figure 4 `duplex-enriched.ifc` coloured by operational carbon (synthetic values) through a viridis gradient normalised over the column. The graph on the left is the whole description._

![Figure 5](../figures/figure-6-3d-embodied-carbon.png)

_Figure 5 Embodied carbon, stages A1 to A3 (synthetic values). The roof carries no embodied-carbon set and therefore remains grey, so that the absence about which Q7 asks is visible without a query._

![Figure 6](../figures/figure-7-3d-category.png)

_Figure 6 The `Category` column through the categorical palette, nine categories, with colours assigned by sorted distinct value so that they are stable across reorderings._

Verdicts are displayed in the same manner. Figure 7 shows rule DC-W1 evaluated inside the graph by a `check.rule` node over the door widths read from the model's own `OverallWidth` attribute and then fed to `view3d.color`, and Figure 8 shows the verdict table behind it.

![Figure 7](../figures/figure-8-3d-dc-w1-verdicts.png)

_Figure 7 Rule DC-W1, requiring a leaf width of at least 850 mm: 8 pass and 6 fail, coloured on the doors of the model. The chain in the preview header is the whole graph, from the two DuckDB views through the rule to the colouring._

![Figure 8](../figures/figure-9-dc-w1-verdict-table.png)

_Figure 8 The `check.rule` output: one row per door with `GlobalId`, the width read in metres and in millimetres, the verdict, and the citation._

Text annotation is provided by the property panel. Figure 9 shows a wall picked in the 3D pane: the pane requests that entity's property sets from the host and lists them, the enrichment's `Pset_NRCEmbodiedCarbon` and `Pset_NRCEnergyPerformance` appearing among the authoring tool's own sets, with the run identifier and scenario name that the provenance convention of Section 5.4 requires.

![Figure 9](../figures/figure-13-picked-element-properties.png)

_Figure 9 The picked element's property sets beneath the 3D view: name, class, `GlobalId`, then one section per set. The analytics sets appear beside the Revit-exported ones because they are ordinary property sets in the file._

Aggregates that depend on the spatial structure are obtained from the `StoreyOfEntity` view added to the toolkit's text views for this work. Figure 10 shows the elements per storey that it produces, including the 103 elements on Level 1 that the hand-driven session of Section 8.2 undercounted.

![Figure 10](../figures/figure-10-storey-of-element.png)

_Figure 10 Elements per storey, from a relation graph over the `StoreyOfEntity` view joined to the elements table: Level 1 103, Level 2 93, T/FDN 14, Roof 8._

The same pane, graphs, and recipes run on a real building. Figure 11 shows the private Snowdon Towers sample, 456,598 instances, coloured by category through the `view3d.categoryStyle` recipe node; the walkthrough captures it after the Duplex figures in order to show that nothing in the display path is sized for the small public model.

![Figure 11](../figures/figure-11-snowdon-categories.png)

_Figure 11 Snowdon Towers (private sample) coloured by category. The graph on the left composes eleven recipe nodes; the browser applies the selected branch to the loaded model._

Aggregated views on the same building are obtained from its typed DuckDB export rather than from property sets. Figure 12 shows the door schedule, 142 doors, built from two `duck.query` nodes, a join, and a sort, this being the graph that the dataflow MCP server also builds from tool calls alone in the walkthrough's final step.

![Figure 12](../figures/figure-12-snowdon-door-schedule.png)

_Figure 12 The Snowdon Towers door schedule in the DuckDB workflow page: mark, type, storey, width in metres, and the reason the width is missing where it is missing._

Overall, Figures 1 to 12 show that colour coding, text annotation, and aggregated views are all obtainable from one description, that the description is the same object whether a person or an agent builds it, and that the path holds at 456,598 instances as well as at 38,898 entities.

## 6.3 Viewer comparison

The test kit [23] defines seven steps: load `duplex.ifc`; connect the analytics CSV on `GlobalId`; test numeric and category colouring; display values for a selected element; test totals by level; load a large model and record responsiveness; and record any preprocessing required. The shortlist in Table 5 is drawn from the inventory, and a full row is to be completed for each viewer once the kit has been run against it.

**Table 5** Viewers and libraries considered, with the one row obtained from the test kit.

| Viewer | Licence | Platform | Colour by property | Colour from external table | Property panel | Aggregates | Scripting | Result |
|---|---|---|---|---|---|---|---|---|
| Bonsai (Blender) [11] | GPL | Desktop | Yes | Yes, via Python | Yes | Via Python | Python, IfcOpenShell | To test |
| xBIM Xplorer [14] | CDDL | Windows | Yes | Via plug-in | Yes | No | .NET | To test |
| That Open Components [12] | MIT | Web | Yes | Yes, via JavaScript | Yes | Via code | JavaScript | To test |
| IFClite [15] | MPL-2.0 | Web | Yes | Via code | Yes | No | JavaScript | To test |
| FreeCAD NativeIFC | LGPL | Desktop | Partial | Via Python | Yes | Via Python | Python | To test |
| BIMvision | Freeware | Windows | Yes | Plug-in | Yes | Limited | Plug-in API | To test |
| FZKViewer | Freeware | Desktop | Yes | No | Yes, strong | No | No | To test |
| BimOpenFlow viewer [8] | MIT | Web | Yes (Figures 4 to 7) | Yes, native (Figures 4 to 7) | Yes, on pick (Figure 9) | Yes, native (Figures 1, 2, 10) | Graph and MCP | Tested 2026-09-18: steps 1 to 5 of the kit pass; step 6 with the Snowdon Towers model, 456,598 instances (Figure 11); step 7, IFC is converted to BOS once by the host and cached |

Speckle, which is listed in the statement of work [20], is a platform rather than a viewer. Its web viewer supports colouring by property and its connectors support custom data, and it should be included in the test run.

## 6.4 Recommendation in brief

In summary, it is recommended that five measures be adopted for the display of analytics:

1. Colour coding should be driven by a value table joined on `GlobalId`, with a gradient for numeric metrics and a categorical palette for classes and verdicts, and unmatched elements should be drawn grey;
2. The selected element's Layer 1 property sets should be shown in a standard property panel, and custom scene labels should not be built for the proof of concept;
3. An aggregated table or bar chart per storey and per category should be provided beside the model, from the same table that drives the colouring;
4. For a screenshot-level deliverable, Layer 1 property sets should be written and any viewer that colours by property used; for an interactive deliverable, the toolkit's dataflow graph and web viewer should be used, these performing the join, the colouring, and the aggregation from one description;
5. Bonsai should be chosen as the reference desktop viewer for verification, because it exposes the full IFC through IfcOpenShell and is able to reproduce the join in a few lines of Python.
