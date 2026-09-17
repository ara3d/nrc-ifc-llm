# 9. Roadmap for an open bidirectional viewer

The statement of work asks for a possible roadmap for a future open-source, bidirectional
viewer. "Bidirectional" means that the viewer not only displays analytics but can write
selections, colourings, verdicts, and overrides back to the model in a form other tools read.

## 9.1 What exists

The toolkit's web viewer is a WebGL viewer built on three.js that knows nothing about IFC or
BOS; the dataflow graph feeds it instance tables with colour columns. The graph is edited by
people and agents through the same four operations, and one MCP server exposes those
operations. The byte-exact writer puts property sets back into the IFC. The pieces of a
bidirectional viewer therefore exist; what is missing is the set of operations that make the
viewer itself something an agent can drive, and the round trip from a click in the viewer to a
property in the file.

## 9.2 Operations the viewer should expose

The MCP survey concluded that a strong core would have about fifteen tools rather than one per
IFC entity type. For the viewer the equivalent set is:

| Operation | Direction | Purpose |
|---|---|---|
| `select` | in | Set the current selection from a `GlobalId` list or a query |
| `get_selection` | out | Return the current selection as a table |
| `color_by` | in | Colour instances from a value table and column, with a colour map |
| `isolate`, `hide`, `section` | in | Reduce the scene to what matters for the question |
| `set_viewpoint`, `get_viewpoint` | in, out | Camera as data, exportable as BCF |
| `annotate` | in | Attach a label or a verdict marker to an element |
| `snapshot` | out | A PNG of the current view, with the graph hash that produced it |
| `write_psets` | in | Persist a table of (element, set, property, value) into the IFC |

Each of these is a node in the dataflow graph as well as a tool, so a colouring an agent
produced is a graph a person can edit, and a person's manual selection is a table an agent can
query.

## 9.3 Stages

**Stage 1: viewer as a graph sink (largely done).** Colour, isolate, section, and explode from
the graph. Selection flows one way, from graph to viewer.

**Stage 2: selection as data.** Clicking in the viewer produces a table on a graph node. "Sum the
carbon of what I have selected" becomes a two-node graph. Viewpoints are exported as BCF so that
issues raised in the viewer can be opened in any BCF-aware tool.

**Stage 3: write-back from the viewer.** A verdict override, a reviewed-by stamp, or a corrected
value entered in the property panel becomes a `sink.writePsets` run: staged, diffed, and applied
only on an explicit run, with the entity diff shown before it is written.

**Stage 4: multi-model and history.** Load two versions of a model and colour by difference in a
metric. Load a portfolio and query across it. This depends on the identifier and epoch work in
Section 8.5.

## 9.4 Constraints to keep

- The viewer stays format-agnostic; IFC knowledge lives in the loaders and the graph.
- Every write to a file happens through the byte-exact path and only inside a run.
- Every image the viewer produces carries the hash of the graph and inputs that produced it.
- The same operations serve the mouse, the HTTP API, and the agent, so there is one path to
  test and one to secure.
