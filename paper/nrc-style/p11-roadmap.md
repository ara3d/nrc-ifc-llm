# 11 Roadmap for an open bidirectional viewer

The statement of work [20] asks for a possible roadmap for a future open-source bidirectional viewer. The term "bidirectional" is used here to mean that the viewer not only displays analytics but is able to write selections, colourings, verdicts, and overrides back to the model in a form that other tools read.

## 11.1 What exists

The toolkit's web viewer is a WebGL viewer built on three.js which knows nothing of IFC or BOS; the dataflow graph feeds it instance tables with colour columns. The graph is edited by people and by agents through the same four operations, and one MCP server exposes those operations. The byte-exact writer returns property sets to the IFC. The components of a bidirectional viewer therefore exist. What is absent is the set of operations that would make the viewer itself something an agent is able to drive, together with the round trip from a click in the viewer to a property in the file.

## 11.2 Operations the viewer should expose

The MCP survey [24] concluded that a strong core would comprise approximately fifteen tools rather than one per IFC entity type. The equivalent set for the viewer is given in Table 12.

**Table 12** Operations a bidirectional viewer should expose.

| Operation | Direction | Purpose |
|---|---|---|
| `select` | In | Set the current selection from a `GlobalId` list or from a query |
| `get_selection` | Out | Return the current selection as a table |
| `color_by` | In | Colour instances from a value table and column, with a colour map |
| `isolate`, `hide`, `section` | In | Reduce the scene to what matters for the question |
| `set_viewpoint`, `get_viewpoint` | In, out | Camera as data, exportable as BCF [3] |
| `annotate` | In | Attach a label or a verdict marker to an element |
| `snapshot` | Out | A PNG of the current view, with the graph hash that produced it |
| `write_psets` | In | Persist a table of element, set, property, and value into the IFC |

Each of these operations is a node in the dataflow graph as well as a tool, so that a colouring produced by an agent is a graph a person is able to edit, and a person's manual selection is a table an agent is able to query.

## 11.3 Stages

**Stage 1: the viewer as a graph sink.** Colour, isolate, section, and explode are driven from the graph, and selection flows one way, from graph to viewer. This stage is largely complete.

**Stage 2: selection as data.** Clicking in the viewer produces a table on a graph node, so that "sum the carbon of what I have selected" becomes a two-node graph. Viewpoints are exported as BCF [3], so that issues raised in the viewer may be opened in any BCF-aware tool.

**Stage 3: write-back from the viewer.** A verdict override, a reviewed-by stamp, or a corrected value entered in the property panel becomes a `sink.writePsets` run, staged, diffed, and applied only on an explicit run, with the entity diff shown before it is written.

**Stage 4: multiple models and history.** Two versions of a model are loaded and coloured by difference in a metric, and a portfolio is loaded and queried across. This stage depends upon the identifier and epoch work described in Section 10.5.

## 11.4 Constraints to be retained

Four constraints should be retained throughout. The viewer should remain format-agnostic, IFC knowledge residing in the loaders and in the graph. Every write to a file should be performed through the byte-exact path and only inside a run. Every image the viewer produces should carry the hash of the graph and of the inputs that produced it. And the same operations should serve the mouse, the HTTP API, and the agent, so that there is one path to test and one to secure.

# 12 Conclusions

The question set by the engagement was how building analytics computed outside IFC may be stored with the model, shown on its geometry, and asked about in plain language. The answer given in this report has three parts, which fit together.

Summaries should be stored in the file and the full data beside it. Custom property sets carry the scalar values that people inspect, with units, stage, scenario, and run identifier in every set, at element, space, storey, and building level. An `IfcDocumentReference` points to a long-format Parquet table joined on `GlobalId` for everything else. A short metric dictionary ties the two together. Writing is performed as a byte-exact patch, so that an enriched file differs from the original only in the entities that were added, and so that those entities may be removed to recover the original exactly. The one correction required is that the aggregate sets be given names of their own, for the reason given in Section 8.2.

The display should be driven from tables rather than from the file. A value table joined on `GlobalId` drives colour, selection detail, and per-storey aggregates from one description, and unmatched elements are drawn grey so that missing data is visible.

The language model should be placed behind tools. A small, typed, read-only tool surface over a columnar copy of the model permits the model to write queries that are correct, checkable, and inexpensive. Answers carry their derivation. Compliance rules are queries with a verdict column, and the absence of data is a verdict rather than a silent pass.

Both case studies were executed. Case study B showed the pipeline working end to end on a public model without the language model in the loop: four rules from a machine-readable file, 56 verdicts in four categories with evidence, an exact match to independently derived ground truth, hash-identical output across runs, and a human override recorded in the IFC and removed again byte for byte. Case study A enriched the same model with 664 property sets and 2,438 typed values and answered eight natural-language questions through the tool surface, seven of eight matching the independently computed expectation in the hand-driven session and four of eight in the unattended run, with three of the four misses traced to one defect in the property naming of Annex A. The viewer comparison remains to be completed for all but one row.

In summary, what the client gains is not a viewer and not a checker but a shape for the data: a row keyed by `GlobalId` which may be a carbon value, a verdict, or an override, and which may be coloured, summed, asked about, validated by an IDS, and written back. Everything described in Sections 10 and 11, from IDS alignment through knowledge graphs to a bidirectional viewer, builds upon that shape rather than replacing it.
