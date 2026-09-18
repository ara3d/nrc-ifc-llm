# 4. Display options and recommendation

This section answers the second objective: how analytics should be shown on IFC geometry, and
what freely available software supports it. The viewer inventory in
[ifc-viewers.md](../ifc-viewers.md) lists the candidates; this section selects among them.

> **Status.** Every figure in this section was captured on 2026-09-18 by the toolkit's
> walkthrough script (`scripts/nrc-walkthrough.mjs`, toolkit commit `66df499`) from the seeded
> graphs in `samples/nrc-analyses`; the captures and their captions are indexed in
> [poc/results/walkthrough-index.md](../poc/results/walkthrough-index.md). The 3D views load
> because the toolkit's IFC-to-BOS converter now drops a non-finite instance transform
> (toolkit commit `53a69d9`) and the web loader hides one instead of rejecting the model
> (`53129a8`). The comparison matrix in 4.3 has one row filled, the toolkit's own viewer; the
> other viewers have not been run through the [test kit](../IFC-Test-Kit/README.md).

## 4.1 Three ways to show a number on a building

**Colour coding.** Each element is coloured by a value. Numeric values map through a gradient
(low to high embodied carbon); categorical values map to a palette (analysis category, pass or
fail). This is the most immediate view and the one every stakeholder understands.

**Text annotation.** The value is shown as text: in a property panel when an element is
selected, as a label in the 3D scene, or as a tooltip. Property panels are universal; scene
labels are rare in free viewers and clutter quickly.

**Aggregated views.** Values are summed or averaged by storey, zone, or category and shown as a
table or chart beside the model, or as a colouring of the containers themselves (storey slabs
coloured by total carbon). This is the view for decisions: which floor, which system, which
option.

The three are not alternatives. A working display shows all three: the model coloured by
metric, the selected element's values in a panel, and a per-storey table alongside.

## 4.2 Where the values come from

Section 3 stored values in property sets (Layer 1) and in an external table (Layer 2). The
display can be driven from either.

- **From property sets.** Any viewer that can colour by property works without extra software.
  This is the path for a screenshot-level demonstration and for handing a file to someone with
  their own viewer. Its limit is that it only shows what was written into the file.
- **From the external table.** The viewer, or a script in front of it, joins the table to the
  geometry on `GlobalId` and colours by any column. This shows any metric, any scenario, without
  rewriting the IFC. It requires a viewer with a scripting or data-binding interface.

The toolkit's dataflow graph does the second. A three-node graph loads the instances of a model,
aggregates or joins a value table, and colours the instances:

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

The `view3d.color` node maps a numeric column through a gradient normalised over its range, or a
text column through a categorical palette with indices assigned by sorted distinct value, so
that colours are stable when rows are reordered. Instances with no match in the value table are
drawn grey, which makes missing data visible rather than silently zero. Changing
`valueColumn` to `energy_intensity` or `colorMap` to `redgreen` re-colours the model without
touching the file.

Aggregated views come from the same graph: a `table.aggregate` node grouped by `Level` feeds a
`chart.bar` or a `view.table` node, and the same aggregate can feed a second `view3d.color`
that colours storeys. Figures 2 and 3 show the storey aggregates from the proof of concept as
a bar chart and as a table, from a two-node graph; Figure 4 shows the property values that
were written into the model, as a table.

![Figure 2. Embodied and operational carbon per storey as a bar chart](figures/figure-2-storey-carbon-chart.png)

_Figure 2. The storey aggregates of the synthetic dataset, drawn by a `chart.bar` node fed from
the storey CSV. The graph on the left is the whole description; the chart is its live output._

![Figure 3. The same aggregates as a table](figures/figure-3-storey-carbon-table.png)

_Figure 3. The same node's output in the Table tab. Building, storey, and roof values are the
ones written into the corresponding IFC entities._

![Figure 4. Property values written into the model](figures/figure-4-property-values-table.png)

_Figure 4. The rows given to the byte-exact writer: entity id, set name, property name, IFC
value type, and value. Each row became one `IFCPROPERTYSINGLEVALUE`._

The 3D colourings of the Duplex model by these values are Figures 5 to 7. Each is a
three-node graph: `view3d.instances` over the enriched IFC, `csv.read` over the elements
table, and `view3d.color` joining them on `GlobalId`. Of the 218 analysed elements, 216 have
a mesh in the converted geometry and are coloured; openings and spaces have no row in the
table and are grey.

![Figure 5. The Duplex model coloured by operational carbon](figures/figure-5-3d-operational-carbon.png)

_Figure 5. `duplex-enriched.ifc` coloured by operational carbon (synthetic values) through a
viridis gradient normalised over the column. The graph on the left is the whole description._

![Figure 6. The same model coloured by embodied carbon A1-A3](figures/figure-6-3d-embodied-carbon.png)

_Figure 6. Embodied carbon A1-A3 (synthetic). The roof has no embodied-carbon set, so it stays
grey: the absence that Q7 asks about is visible without a query._

![Figure 7. One colour per analysis category](figures/figure-7-3d-category.png)

_Figure 7. The `Category` column through the categorical palette, nine categories, colours
assigned by sorted distinct value so they are stable across reorderings._

Verdicts are displayed the same way. Figure 8 is rule DC-W1 evaluated inside the graph by a
`check.rule` node over the door widths read from the model's own `OverallWidth`, then fed to
`view3d.color`; Figure 9 is the verdict table behind it.

![Figure 8. DC-W1 verdicts coloured on the doors](figures/figure-8-3d-dc-w1-verdicts.png)

_Figure 8. Rule DC-W1 (leaf width at least 850 mm): 8 pass, 6 fail, coloured on the doors of
the model. The chain in the preview header is the whole graph, from the two DuckDB views
through the rule to the colouring._

![Figure 9. The verdict table](figures/figure-9-dc-w1-verdict-table.png)

_Figure 9. The `check.rule` output: one row per door with `GlobalId`, the width read in
metres and millimetres, the verdict, and the citation._

Text annotation is the property panel. Figure 13 is a wall picked in the 3D pane: the pane
asks the host for that entity's property sets and lists them, the enrichment's
`Pset_NRCEmbodiedCarbon` and `Pset_NRCEnergyPerformance` among the authoring tool's own, with
the run identifier and scenario name the provenance convention requires.

![Figure 13. A picked wall's property sets](figures/figure-13-picked-element-properties.png)

_Figure 13. The picked element's property sets under the 3D view: name, class, `GlobalId`,
then one section per set. The analytics sets sit beside the Revit-exported ones because they
are ordinary property sets in the file._

Aggregates that depend on the spatial structure come from the `StoreyOfEntity` view added to
the toolkit's text views for this work; Figure 10 shows the elements per storey it produces,
including the 103 on Level 1 that the hand-driven session in Section 6.2 undercounted.

![Figure 10. Elements per storey from the StoreyOfEntity view](figures/figure-10-storey-of-element.png)

_Figure 10. Elements per storey, from a relation graph over the `StoreyOfEntity` view joined to
the elements table: Level 1 103, Level 2 93, T/FDN 14, Roof 8._

The same pane, graphs, and recipes run on a real building. Figure 11 is the private Snowdon
Towers sample, 456,598 instances, coloured by category through the `view3d.categoryStyle`
recipe node; the walkthrough captures it after the Duplex figures to show that nothing in the
display path is sized for the small public model.

![Figure 11. Snowdon Towers coloured by category](figures/figure-11-snowdon-categories.png)

_Figure 11. Snowdon Towers (private sample) coloured by category. The graph on the left composes
eleven recipe nodes; the browser applies the selected branch to the loaded model._

Aggregated views on the same building come from its typed DuckDB export rather than from
property sets: Figure 12 is the door schedule (142 doors) built from two `duck.query` nodes, a
join, and a sort, the graph the dataflow MCP server also builds from tool calls alone in the
walkthrough's last step.

![Figure 12. The Snowdon door schedule](figures/figure-12-snowdon-door-schedule.png)

_Figure 12. The Snowdon door schedule in the DuckDB workflow page: mark, type, storey, width in
metres, and why the width is missing when it is._

## 4.3 Viewer comparison

The test kit defines seven steps: load `duplex.ifc`, connect the analytics CSV on `GlobalId`,
test numeric and category colouring, display values for a selected element, test totals by
level, load a large model and record responsiveness, and record any preprocessing required.
The shortlist below is drawn from the inventory; a full row is filled in for each once the kit
has been run.

| Viewer | Licence | Platform | Colour by property | Colour from external table | Property panel | Aggregates | Scripting | Result |
|---|---|---|---|---|---|---|---|---|
| Bonsai (Blender) | GPL | Desktop | Yes | Yes, via Python | Yes | Via Python | Python, IfcOpenShell | to test |
| xBIM Xplorer | CDDL | Windows | Yes | Via plug-in | Yes | No | .NET | to test |
| That Open Components | MIT | Web | Yes | Yes, via JavaScript | Yes | Via code | JavaScript | to test |
| IFClite | MPL-2.0 | Web | Yes | Via code | Yes | No | JavaScript | to test |
| FreeCAD NativeIFC | LGPL | Desktop | Partial | Via Python | Yes | Via Python | Python | to test |
| BIMvision | Freeware | Windows | Yes | Plug-in | Yes | Limited | Plug-in API | to test |
| FZKViewer | Freeware | Desktop | Yes | No | Yes, strong | No | No | to test |
| BimOpenFlow viewer (toolkit) | MIT | Web | Yes (Figures 5 to 8) | Yes, native (Figures 5 to 8) | Yes, on pick (Figure 13) | Yes, native (Figures 2, 3, 10) | Graph and MCP | tested 2026-09-18: steps 1 to 5 of the kit pass; step 6 with the Snowdon model, 456,598 instances (Figure 11); step 7: IFC is converted to BOS once by the host and cached |

Speckle, listed in the statement of work, is a platform rather than a viewer; its web viewer
supports colouring by property and its connectors support custom data, and it should be
included in the test run.

## 4.4 Recommendation in brief

1. Use colour coding driven by a value table joined on `GlobalId`, with a gradient for numeric
   metrics and a categorical palette for classes and verdicts. Draw unmatched elements grey.
2. Show the selected element's Layer 1 property sets in a standard property panel; do not build
   custom scene labels for the proof of concept.
3. Provide an aggregated table or bar chart per storey and per category beside the model, from
   the same table that drives the colouring.
4. For a screenshot-level deliverable, write Layer 1 property sets and use any viewer that
   colours by property. For an interactive deliverable, use the toolkit's dataflow graph and
   web viewer, which do the join, the colouring, and the aggregation from one description.
5. Choose Bonsai as the reference desktop viewer for verification, because it exposes the full
   IFC through IfcOpenShell and can reproduce the join in a few lines of Python.
