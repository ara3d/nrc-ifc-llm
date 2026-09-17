# 4. Display options and recommendation

This section answers the second objective: how analytics should be shown on IFC geometry, and
what freely available software supports it. The viewer inventory in
[ifc-viewers.md](../ifc-viewers.md) lists the candidates; this section selects among them.

> **Status.** The comparison matrix in 4.3 records the intended tests from the
> [IFC viewer test kit](../IFC-Test-Kit/README.md). The cells marked "to test" have not been
> filled in, and no screenshots have been captured yet. The section will be completed once the
> test kit has been run through the shortlisted viewers.

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
that colours storeys.

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
| BimOpenFlow viewer (toolkit) | MIT | Web | Yes | Yes, native | Yes | Yes, native | Graph and MCP | in use |

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
