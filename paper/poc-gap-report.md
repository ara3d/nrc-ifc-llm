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
| Colour coding on 3D geometry from a value table | Figures 5 to 8, captured 2026-09-18 after the converter and loader fixes (see 2.2) | Done |
| Property panel on a selected element | The toolkit's 3D pane shows the picked element's property sets (toolkit, 2026-09-18); screenshot pending | In progress |
| Viewer comparison from the test kit | One row, the toolkit viewer, from the walkthrough; other viewers not run | Partly done |
| Autonomous LLM agent answering unattended | `gpt-5` through `bimopenmcp-ifc-ask`, 2026-09-18: four of eight match, transcript in `poc/results/transcript-unattended.md` | Done, with three misses explained in Section 6.2 |

## 2. Gaps found

### 2.1 The agent was the author (unattended runner added 2026-09-18)

The questions were answered by choosing MCP tool calls by hand and recording each call and
result before writing the answer. This proves the tool surface can answer the paper's
question list from the enriched file. It does not measure how a language model performs
unattended. The toolkit now has `bimopenmcp-ifc-ask` (`src/studio/BimOpenMcp.Ifc.Ask`), which
runs a question list unattended through the same agent loop as the DuckDB Ask box, against
the IFC MCP server in process, one fresh conversation per question, and records every tool
call; `samples/nrc/questions.txt` holds this paper's eight questions. The run of 2026-09-18
is in Section 6.2: the misses come from the storey and building aggregates sharing the element
property names, which is a storage-design finding (see 2.10).

### 2.2 The 3D viewer rejected the Duplex model (resolved 2026-09-18)

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

Resolution: the cause was one zero-vertex mesh whose translation web-ifc reports as infinity;
the toolkit's converter now skips zero-vertex meshes and non-finite transforms (commit
`53a69d9`), and the web loaders hide such an instance and report it as skipped instead of
rejecting the model (`53129a8`). The colouring graphs were moved into the toolkit as
`samples/nrc-analyses/nrc-color-*` with tests (`21e6b52`), and Figures 5 to 8 were captured by
`scripts/nrc-walkthrough.mjs` (`66df499`).

### 2.3 No `IfcDocumentReference` was written (builder added 2026-09-18)

Layer 2 is referenced from the project through properties in `Pset_NRCAnalyticsProvenance`
(`ResultDatasetURI`, `ResultDatasetFormat`, `JoinKey`). The recommendation in Section 3.4 calls
for an `IfcDocumentReference` associated through `IfcRelAssociatesDocument`. The toolkit now has
`IfcDocumentReferenceBuilder` (commit `6b34a54`), which emits `IFCDOCUMENTINFORMATION`,
`IFCDOCUMENTREFERENCE`, and `IFCRELASSOCIATESDOCUMENT` with the IFC2X3 or IFC4 attribute
layout, tested against the Duplex project entity for an exact diff and byte-for-byte reversal.
The enriched file in `poc/data` was not rewritten with it; doing so is one call in
`poc/EnrichIfc/Program.cs`.

### 2.4 The `bim` host profile could not load a CSV

The host's `bim` profile registered the geometry, BOS, compliance, effects, and viz packs but
not the DuckDB or Tables packs, so a `csv.read` node was an unknown kind and no external value
table could drive a colouring. A one-line change adds the two packs to the profile; the host
tests pass with it. This is committed to the toolkit as part of this run. The Tables-profile
tests that pin its exact contents are unaffected.

### 2.5 Storey resolution through relations missed assembly parts (view added)

The converted model's `ContainedIn` relation points at rooms for elements inside a room and at
the storey for others, and stair, railing, and member parts are reached only through
`PartOf`. The Q2 query walked room to storey but not assembly to element, reached 93 of 103
Level 1 elements, and reversed a marginal comparison. The toolkit's text views now include
`StoreyOfEntity`, which walks `ContainedIn`, `PartOf`, and `MemberOf` (the Duplex conversion
emits aggregation as `MemberOf`); the seeded graph `nrc-storey-of-element` reaches all 103
Level 1 elements (Figure 10), and the IFC MCP server exposes the same view to `ifc_sql`.

### 2.6 `sink.writePsets` wrote every value as text (resolved)

The dataflow node writes `IFCTEXT` for every value, so numeric analytics written through a
graph would read back as strings. The proof of concept bypassed the node and called the
library directly to get `IFCREAL`. The node now accepts an optional `valueType` column, and the seeded graph `nrc-enrich-run`
writes `psets_to_write.csv` with its types under an engine Run.

### 2.7 Names are ambiguous keys

Four doors share the family name used in Q4. The agent listed all four rather than picking
one, which is the right behaviour, but the question list should use `GlobalId` for
component-level questions, and the paper's Section 6.2 should say so.

### 2.8 One toolkit test failed on this machine independently of the change (resolved)

`BimSampleSeedingTests.EmptyStore_SeedsBimAndView3dSamples` expects the seeded list to end
without a Snowdon entry, and fails wherever the private Snowdon file is present. It fails with
and without the profile change. The test now includes the Snowdon ids only when the local model exists.

### 2.9 Windows only

The IFC loader, the MCP server, and the write path target `net8.0-windows`. Nothing in this
run could be repeated on Linux or macOS.

### 2.10 Aggregates share the element property names (found by the unattended run)

`Pset_NRCOperationalCarbon.OperationalCarbon_kgCO2e_per_year` is written on elements, on
storeys, and on the building. A sum or ranking over the property that does not exclude the
container classes counts the aggregates as elements (Q3, Q5) and doubles per-storey sums
(Q8). Appendix A should give the aggregate sets distinct names, and the generator, the
enrichment, and the expected answers should be rerun with them.

## 3. What to do next, in order

Items 1 to 5 of the original list were done in the toolkit on 2026-09-18 (sections 2.1, 2.2,
2.3, 2.5, 2.6 above). What remains:

1. Rename the storey and building aggregate sets (2.10), regenerate, re-enrich, and rerun the
   unattended questions; then quote the match count in the abstract.
2. Rewrite the enriched file with the `IfcDocumentReference` and re-verify the diff and hash.
3. Run the viewer test kit through the rest of the shortlist in Section 4.3 (Bonsai first).
4. Repeat the run on an NRC model with real analytics.
