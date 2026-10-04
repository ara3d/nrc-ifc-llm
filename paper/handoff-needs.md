# Handoff: what the paper still needs

_Written 2026-09-18 for whoever picks this up next, human or agent. Self-contained: it names
every file, command, and acceptance check. Read [paper/README.md](README.md) for the paper's
shape and [poc-gap-report.md](poc-gap-report.md) for how the current gaps were found._

## The goal in one paragraph

The paper (deliverable D3 of the NRC statement of work) claims that building analytics can be
stored in IFC property sets and travel with the file, displayed on the geometry from the same
tables, and queried in plain language through a small tool surface. The acceptance criteria in
[statement-of-work.md](../statement-of-work.md) section 6 are: an options analysis at
component, zone, storey, and building level with recommendations; a proof of concept in which
natural-language questions are answered against an analytics-enriched IFC model; a paper that
passes the client's editorial review; and a presentation. The options analysis and the paper
draft exist. The proof of concept is partly done. This document says what "done" means at two
levels.

## Where things are

| Thing | Location |
|---|---|
| Paper, one file per section | `paper/*.md`, index in `paper/README.md` |
| Figures | `paper/figures/` (Figure 1 SVG, Figures 2 to 4 PNG, one gap screenshot) |
| Proof of concept scripts, data, results | `poc/` with its own `README.md` |
| Enriched model | `poc/data/duplex-enriched.ifc` (SHA-256 in `poc/results/enrich-report.json`) |
| Recorded question session | `poc/results/transcript.md` |
| Expected answers | `poc/results/expected_answers.json` |
| Dataflow graphs for figures | `poc/graphs/*.json` |
| Toolkit used | sibling clone `../bim-open-toolkit`, at commit `66df499` or later for the walkthrough |
| Walkthrough that regenerates every figure and MCP transcript | `npm run nrc:walkthrough --prefix bimopenflow/web` in the toolkit; narrative in its `docs/nrc-walkthrough.md`; output index copied to `poc/results/walkthrough-index.md` |
| Launch entries for host and web editor | `.claude/launch.json` (host on 5214, web on 5300) |
| Earlier executed evidence (door clearance) | `door-clearance-demo.md`, `bos-validation-evidence.md` |

The toolkit's layout as of 2026-10-04 (tag `v0.1`, after the repository split): `deps/bim-open-data/src/data` (IFC loader, byte-exact editing, BOS),
`deps/bim-open-flow/src/flow` (dataflow host and node packs), `deps/bim-open-data/src/mcp/BimOpenMcp.Ifc` (the IFC MCP server),
`viz` (web viewer packages, with Playwright under `viz/node_modules/playwright-core`),
`bimopenflow/web` (the editor). Everything that touches IFC targets `net8.0-windows`.

## Minimal: what the paper needs to be defensible

Each item has a check that says when it is done. Do them in this order.

### M1. A 3D colour-coded figure on the public model (done 2026-09-18)

Done in the toolkit: converter fix `53a69d9`, loader tolerance `53129a8`, the colouring graphs
as seeded samples with tests `21e6b52`, and the walkthrough that captures them `66df499`.
Figures 5 to 10 are in `paper/figures/` and Section 4 cites them. The original notes follow.

The paper's display recommendation (Section 4) has no picture of analytics on geometry. The
graphs exist and the host accepts them; the viewer fails to load `duplex.ifc`.

- Symptom: the 3D pane shows `The BOS archive could not be prepared: Invalid BFAST transform 495`
  for `duplex.ifc` and for `duplex-enriched.ifc`. Screenshot in
  `paper/figures/gap-3d-pane-duplex-error.png`.
- Where it is thrown: `bim-open-toolkit/deps/bim-open-viewer/packages/loaders/src/bfast-loader.ts` line 36,
  when any of the 16 floats of an instance transform is not finite.
- Where the bad value comes from: the host's IFC-to-BOS geometry conversion behind
  `GET /api/models/{id}/bos` in `deps/bim-open-flow/src/flow/BimOpenFlow.Host.Api/ModelBytesEndpoint.cs`. Find
  which Duplex instance produces the NaN or infinity (instance index 495 in the converted
  archive; the index changes if you exclude openings) and fix the converter. Also make the
  loader skip or flag a bad instance rather than abort the model, so one bad transform can
  never blank a whole building again.
- Then start the host and editor from `.claude/launch.json`, load the graphs with a PUT per
  file to `http://127.0.0.1:5214/api/analyses/{id}` (see the loop in `poc/README.md` or the
  Python snippet at the end of this document), and run:

```bash
node poc/screenshots.mjs
```

- Add captures for `nrc-color-operational-carbon`, `nrc-color-embodied-carbon`,
  `nrc-color-category`, and `nrc-door-verdicts-dc-w1` on the `3D` tab to the `captures` list
  in `poc/screenshots.mjs`, named Figure 5 onwards.
- Done when: four PNGs exist showing the Duplex model coloured, unmatched elements grey, and
  Section 4 cites them in place of the sentence that says the viewer could not load the model.

### M2. An unattended language-model run of the question list (done 2026-09-18)

The runner is `bimopenmcp-ifc-ask` in the toolkit (`f4bb2fa`, tests `13463b2`), with the
question list in `samples/nrc/questions.txt`. Build with
`npm run ifc:ask-build --prefix bimopenflow/web`, set `OPENAI_API_KEY_FILE`, and run it with
`--model samples/nrc/duplex-enriched.ifc --questions samples/nrc/questions.txt --out ... --results ...`.
It writes the transcript and a JSON results file with model name, tool calls, turns, and
tokens per question; Section 6.2 reports the recorded run. The original notes follow.

The transcript in `poc/results/transcript.md` was produced by the author choosing tool calls
by hand. The acceptance criterion says questions are answered by an LLM-based agent.

- Start the server: from the toolkit root,
  `dotnet run --project deps/bim-open-data/src/mcp/BimOpenMcp.Ifc -- --http 8766` (or stdio for a chat client).
- Register it with any MCP client that runs a model unattended (Claude Code with an
  `mcpServers` entry, or the toolkit's Ask loop pattern in
  `deps/bim-open-flow/src/studio/BimOpenFlow.Ask/AskAgent.cs` adapted to this server).
- Ask the eight questions in `paper/06-proof-of-concept.md` section 6.2 verbatim, one at a
  time, against `poc/data/duplex-enriched.ifc`. Save the raw transcript as
  `poc/results/transcript-unattended.md`.
- Compare each answer with `poc/results/expected_answers.json`. Record model name, tool calls
  per question, and match or mismatch in a table.
- Done when: Section 6.2 has a second results table headed with the model name, and Section 7
  no longer says the agent was the author.

### M3. Two sentences of real data provenance, or an explicit synthetic label everywhere

The values are synthetic. Either NRC supplies one real analytics dataset for one model and the
run is repeated on it, or every figure caption, table, and the abstract must say "synthetic"
where a number appears. The abstract currently does not.

- If real data arrives: rerun `poc/generate_synthetic_analytics.py` replaced by a loader for
  the real columns (keep the output file names so `EnrichIfc`, `expected_answers.py`, and the
  graphs work unchanged), rerun the three commands in `poc/README.md`, and re-record M2.
- Done when: either the run is on real data, or a search for numbers in
  `paper/00-abstract.md` and every figure caption finds the word synthetic next to them.

### M4. Viewer comparison, at least three rows filled (one row done)

The toolkit viewer row is filled from the walkthrough (Section 4.3); the toolkit's 3D pane now
shows the picked element's property sets, which covers the kit's step 4 for that viewer. Bonsai
and one web viewer remain.

Section 4.3 is a table of "to test". The test kit in `IFC-Test-Kit/README.md` gives seven
steps. Run them in Bonsai, in one web viewer (That Open Components or IFClite), and in the
toolkit's own viewer once M1 is fixed. Fill the rows; add one screenshot per viewer showing
the enriched property sets in its property panel (this also closes the "property panel not
attempted" gap).

- Done when: three rows have no "to test" cell, and Section 4.4's recommendation cites them.

### M5. Editorial pass

Concatenate with the command in `paper/README.md`, read once end to end, and fix: the Q2
narrative in 6.2 and 7.1 must agree; every figure number is cited in order; every section
that says "will be reported in the next revision" is updated or removed; the references list
has a real citation for the Duplex model and the NBC.

## Ideal: what would make the paper strong

These go beyond the acceptance criteria. Each is independent; pick by value.

### I1. Write the Layer 2 reference as an `IfcDocumentReference` (builder done)

`IfcDocumentReferenceBuilder` landed in the toolkit (`6b34a54`); what remains is calling it from
`poc/EnrichIfc/Program.cs` and re-verifying. The original notes follow.

Section 3.4 recommends it; the run only wrote the URI into a property set. Extend
`IfcPropertySetBuilder` in `bim-open-toolkit/deps/bim-open-data/src/data/Ara3D.Ifc.Editing` with a method that
emits `IFCDOCUMENTINFORMATION`, `IFCDOCUMENTREFERENCE`, and `IFCRELASSOCIATESDOCUMENT` for a
project or building entity, following the same deterministic-GUID pattern. Add it to
`poc/EnrichIfc/Program.cs` and re-verify the diff, reversal, and hash. Cite the STEP lines in
Appendix A.

### I2. A storey-of-element view in the BOS text views (done)

`StoreyOfEntity` exists in `BosDuckDbViews.cs` and `IfcDuck.cs`; the seeded graph
`nrc-storey-of-element` and Figure 10 use it. The original notes follow.

The Q2 miss came from walking `ContainedIn` but not `PartOf`. Add a `StoreyOfEntity` view in
`bim-open-toolkit/deps/bim-open-data/src/mcp/BimOpenMcp.Ifc/IfcDuck.cs` (next to `EntityText`, `ParameterText`,
`RelationText`) that resolves every entity to its storey through both relations. Rerun Q2;
the agent should then get 103 Level 1 elements and the expected ordering.

### I3. Typed values through `sink.writePsets` (done)

The node takes a `valueType` column; `nrc-enrich-run` is the one-graph enrichment. The original
notes follow.

The dataflow node writes every value as `IFCTEXT`
(`bim-open-toolkit/deps/bim-open-flow/src/flow/BimOpenFlow.Nodes.Effects/WritePsetsNode.cs`). Accept an optional
`valueType` column (`Real`, `Integer`, `Boolean`, `Label`, `Identifier`, `Text`) and map it
to `IfcPropertyValue` factories, defaulting to `Text`. Then the whole enrichment can be one
graph: `csv.read` of `poc/data/psets_to_write.csv` into `sink.writePsets`, run inside a Run,
with the run record as provenance. That is a better figure than the console program.

### I4. IDS specification for Layer 1

Author `poc/nrc-analytics.ids` (IDS 1.0 XML) requiring `Pset_NRCOperationalCarbon` and
`Pset_NRCEnergyPerformance` on the element classes in Appendix A, with `AnalysisRunId` and
`ScenarioName` present. Validate `duplex-enriched.ifc` with an existing checker (IfcOpenShell's
`ifctester` is the simplest) and put the pass/fail counts in Section 8.2. This turns the
recommendation's item 6 from future work into evidence.

### I5. Compliance verdicts as a graph, not a test project (done)

`nrc-dc-w1-verdicts` is that graph; Figures 8 and 9 show it. The original notes follow.

Rebuild rule DC-W1 with the compliance node pack (`check.rule` over a table of doors with
`OverallWidth`), colour the model by verdict with `view3d.color`, and write the verdicts back
with `sink.writePsets`. Section 5.5 currently asserts this composition; a figure would show it.

### I6. Mesh-accurate door clearance

Wire `ifc_bounds` or `ifc_volume` into the DC-Z1 zone test in
`bim-open-toolkit/deps/bim-open-data/tests/data/Ara3D.DoorClearance.Tests` so obstacles are tested by geometry
rather than placement origin. Report whether the two obstructed doors change.

### I7. A second public model

Repeat the whole run on `data/AC20-FZK-Haus.ifc` (KIT model, IFC4). It has different authoring
conventions and would show the pipeline is not tuned to Revit-exported IFC2X3.

### I8. Cross-platform

The IFC stack targets `net8.0-windows` only because of the loader project. If the native
web-ifc dependency is the only reason, a Linux build of the MCP server would let reviewers run
the demo. Worth a paragraph in Section 7 either way.

### I9. Fix the environment-dependent toolkit test (done)

`BimSampleSeedingTests.EmptyStore_SeedsBimAndView3dSamples` in
`bim-open-toolkit/tests/studio/BimOpenFlow.BimWorkflows.Tests` fails on any machine that has the
private Snowdon sample. Make it ignore the optional Snowdon entry.

## Rules for whoever does this

- Do not cite a number in the paper that is not in a file under `poc/results/` or pinned to a
  commit. Every executed claim must be reproducible from a command in `poc/README.md`.
- Record tool calls before writing answers. The Q2 answer was wrong once because it was
  written before the result was read; the transcript keeps that on purpose.
- Keep IFC files byte-exact. `.gitattributes` disables line-ending conversion for `*.ifc`;
  do not remove it.
- Commit each item above as its own commit, with the check that proved it in the message.
- If an item cannot be done, say so in `paper/poc-gap-report.md` with the reason, instead of
  softening the claim in the paper.

## Snippet: loading the graphs into a running host

```python
import json, glob, os, urllib.request
for f in sorted(glob.glob("poc/graphs/*.json")):
    gid = os.path.basename(f)[:-5]
    body = open(f, "rb").read()
    req = urllib.request.Request(f"http://127.0.0.1:5214/api/analyses/{gid}", data=body,
                                 method="PUT", headers={"Content-Type": "application/json"})
    print(gid, urllib.request.urlopen(req).status)
```
