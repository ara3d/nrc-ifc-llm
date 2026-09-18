# Proof-of-concept gap report

_Run of 2026-09-17 on the BIM Open Toolkit at commit `afe69b4` plus one local change. This
report lists what the run set out to show, what it showed, and what it did not._

The run is described in [poc/README.md](../poc/README.md). Its purpose was to produce
evidence for the paper's three claims: analytics can be stored in IFC and travel with the
file (Section 3), displayed from the same tables (Section 4), and queried through a small tool
surface (Section 5).

## 1. What was demonstrated

| Requirement | Evidence | Status |
|---|---|---|
| Layer 1 property sets at element, storey, building, project level | 664 sets, 2,438 typed values written into `duplex-enriched.ifc`; `enrich-report.json` | Done |
| Byte-exact, auditable, reversible write | Entity diff equals the additions; removal restores the source byte for byte; second run byte-identical | Done |
| Layer 2 long-format table with provenance | `nrc_analytics_long.csv`; `Pset_NRCAnalyticsProvenance` on the project names it with join key | Done, except the `IfcDocumentReference` entity itself (see 2.3) |
| Natural-language questions at component, storey, building, category, provenance, absence level | 8 questions, 12 tool calls, transcript with every call and result | Done, author as agent (see 2.1) |
| Answers match independent expectation | 7 of 8 exact; Q2 differs because of incomplete storey resolution | Done, with one honest miss |
| Aggregated views (chart, table per storey) | Figures 2 and 3, from a two-node graph over the storey CSV | Done |
| Values shown as a table | Figure 4, the written property values | Done |
| Colour coding on 3D geometry from a value table | Graphs built and accepted by the host; viewer fails to load the Duplex geometry | **Not done** (see 2.2) |
| Property panel on a selected element | Not attempted in a viewer; shown only as MCP output | **Not done** |
| Viewer comparison from the test kit | Not run | **Not done** |
| Autonomous LLM agent answering unattended | Not run | **Not done** |

## 2. Gaps found

### 2.1 The agent was the author

The questions were answered by choosing MCP tool calls by hand and recording each call and
result before writing the answer. This proves the tool surface can answer the paper's
question list from the enriched file. It does not measure how a language model performs
unattended. The toolkit has an unattended Ask loop for the DuckDB profile that needs an
OpenAI key; a comparable run over the IFC MCP server through a chat client is the missing
experiment.

### 2.2 The 3D viewer rejects the Duplex model

Every colouring graph (`nrc-color-operational-carbon`, `-embodied-carbon`, `-category`,
`nrc-door-verdicts-dc-w1`) validates and evaluates on the host, but the 3D pane reports:

```text
The BOS archive could not be prepared: Invalid BFAST transform 495
```

The same error occurs for the original `duplex.ifc`, so the enrichment is not the cause. The
message comes from the viewer's loader (`viz/packages/loaders/src/bfast-loader.ts`), which
throws when any instance transform contains a non-finite number. The host's IFC-to-BOS
geometry path therefore emits at least one NaN or infinite transform for this model, and the
loader aborts the whole model rather than skipping the instance. Two fixes are needed in the
toolkit: find and correct the transform in the converter, and make the loader drop or flag a
bad instance instead of failing the load. Until then the paper has no 3D colour-coded figure
on a public model. The Snowdon sample renders, but it is a private model and its screenshot
cannot be published.

Screenshot of the failure: [gap-3d-pane-duplex-error.png](figures/gap-3d-pane-duplex-error.png).

### 2.3 No `IfcDocumentReference` was written

Layer 2 is referenced from the project through properties in `Pset_NRCAnalyticsProvenance`
(`ResultDatasetURI`, `ResultDatasetFormat`, `JoinKey`). The recommendation in Section 3.4 calls
for an `IfcDocumentReference` associated through `IfcRelAssociatesDocument`. The byte-exact
builder only emits property sets today; adding a document-reference builder is a small
extension of `IfcPropertySetBuilder`.

### 2.4 The `bim` host profile could not load a CSV

The host's `bim` profile registered the geometry, BOS, compliance, effects, and viz packs but
not the DuckDB or Tables packs, so a `csv.read` node was an unknown kind and no external value
table could drive a colouring. A one-line change adds the two packs to the profile; the host
tests pass with it. This is committed to the toolkit as part of this run. The Tables-profile
tests that pin its exact contents are unaffected.

### 2.5 Storey resolution through relations misses assembly parts

The converted model's `ContainedIn` relation points at rooms for elements inside a room and at
the storey for others, and stair, railing, and member parts are reached only through
`PartOf`. The Q2 query walked room to storey but not assembly to element, reached 93 of 103
Level 1 elements, and reversed a marginal comparison. The query layer would benefit from a
`storey-of-element` view in the BOS text views that walks both relations, so an agent does not
have to rediscover this.

### 2.6 `sink.writePsets` writes every value as text

The dataflow node writes `IFCTEXT` for every value, so numeric analytics written through a
graph would read back as strings. The proof of concept bypassed the node and called the
library directly to get `IFCREAL`. The node needs a `valueType` column or type inference.

### 2.7 Names are ambiguous keys

Four doors share the family name used in Q4. The agent listed all four rather than picking
one, which is the right behaviour, but the question list should use `GlobalId` for
component-level questions, and the paper's Section 6.2 should say so.

### 2.8 One toolkit test fails on this machine independently of the change

`BimSampleSeedingTests.EmptyStore_SeedsBimAndView3dSamples` expects the seeded list to end
without a Snowdon entry, and fails wherever the private Snowdon file is present. It fails with
and without the profile change. The test should exclude the optional Snowdon sample.

### 2.9 Windows only

The IFC loader, the MCP server, and the write path target `net8.0-windows`. Nothing in this
run could be repeated on Linux or macOS.

## 3. What to do next, in order

1. Fix the non-finite transform in the IFC-to-BOS geometry path and make the loader tolerant,
   then capture the four colouring figures the graphs already define.
2. Run the question list unattended through a chat client against the IFC MCP server and
   record the transcript alongside the hand-driven one.
3. Add a document-reference builder and write the Layer 2 reference as an
   `IfcDocumentReference`.
4. Add a storey-of-element view to the BOS text views.
5. Pass value types through `sink.writePsets`.
6. Run the viewer test kit through the shortlist in Section 4.3.
7. Repeat the run on an NRC model with real analytics.
