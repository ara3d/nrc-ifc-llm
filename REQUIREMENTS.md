# Requirements

One table of what this repository has to deliver, where each requirement comes from, whether
it is met today, and what checks it. Status was assessed on 2026-10-03 against this
repository's `main` and the BIM Open Toolkit submodule pinned at `34499e3`.

Sources:

- **SOW**: [statement-of-work.md](statement-of-work.md), the contract with the National
  Research Council Canada (NRC).
- **M1–M5, I1–I9**: [paper/handoff-needs.md](paper/handoff-needs.md), the minimal (M) and
  ideal (I) items for the paper.
- **W6**: workflow 6 of the toolkit's brief, `PROJECT.md` in `bim-open-toolkit` at the pin,
  "Reproduce the paper, including the write-back, with one command".

Checks named `paths`, `poc` and `toolkit-nrc` are jobs of
[.github/workflows/check.yml](.github/workflows/check.yml), which runs on every push and pull
request. "None" means nothing checks the requirement, by machine or by a recorded hand run.

## Statement of work

| ID | Requirement and source | Status | Check |
|---|---|---|---|
| SOW-1 | An options analysis of storing and displaying analytics at component, zone, storey and building level, with a comparison matrix and recommendations (SOW §2.1, §2.2, D1, §6 first criterion). | Partly. Paper §3 (storage, matrix in §3.3, recommendation in §3.6) and §4 (display, recommendation in §4.4) cover it. D1 asks for a separate concise brief; none exists outside the paper. | None. |
| SOW-2 | The proof of concept includes an IFC model enriched with analytics through the recommended storage approach (SOW §3.3, D2). | Met. `poc/data/duplex-enriched.ifc`: 664 property sets and 2,438 values written into `IFC-Test-Kit/duplex.ifc` by `poc/EnrichIfc`. | `poc` (see W6-4). |
| SOW-3 | An agent based on a large language model (LLM) answers natural-language questions about the stored carbon, energy and other analytics at component and building level (SOW §3.3, D2, §6 second criterion). | Partly. The unattended `gpt-5` run answered 4 of the 8 questions correctly, 1 partly and 3 wrongly (paper §6.2); the earlier session with hand-chosen tool calls matched 7 of 8. No run with Claude is recorded. | By hand, last run 2026-09-18 (`poc/results/results-unattended.json`). `poc` re-reads the recorded Q2, Q4 and Q6 answers; it calls no model. |
| SOW-4 | A lightweight visualisation colours the model by analytics value (SOW §3.3, D2). | Met. Figures 5 to 8 in `paper/figures/`. | By hand, last run 2026-09-18 (`poc/results/walkthrough-index.md`); `toolkit-nrc` asserts the row and colour counts behind each Duplex figure (`FigureGraphTests`). |
| SOW-5 | The proof-of-concept package carries its source code and documentation (SOW D2). | Met. `poc/README.md` lists every file and the commands that regenerate them. | `paths` (every toolkit path the documentation names exists at the pin) and `poc` (the documented commands run). |
| SOW-6 | The paper covers storage, display, the role of LLM and agent layers, proof-of-concept results, knowledge graphs and world-model substrates as extensions, and a roadmap for an open bidirectional viewer (SOW §3.4). | Met. Paper §3, §4, §5, §6, §8.3 and §8.4, §9. | None. |
| SOW-7 | The paper passes the client's editorial review (SOW D3, §6 third criterion). | Not met. No review is recorded; the editorial pass M5 is still open. | None. |
| SOW-8 | A final presentation and handover to the client team (SOW D4, §6 fourth criterion). | Not met. Nothing in the repository records one. | None. |

## Handoff items for the paper

| ID | Requirement and source | Status | Check |
|---|---|---|---|
| M1 | A 3D colour-coded figure of the public Duplex model (handoff-needs.md, M1). | Met 2026-09-18: Figures 5 to 10 in `paper/figures/`, cited in §4. | Same as SOW-4. |
| M2 | An unattended LLM run of the eight questions, with model name and per-question match in §6.2 (handoff-needs.md, M2). | Met: `gpt-5`, 2026-09-18, toolkit `66df499`; the result is SOW-3's 4 of 8. | By hand, last run 2026-09-18; `poc` checks the recorded Q2, Q4 and Q6 answers. |
| M3 | Every number in the abstract and every figure caption is labelled synthetic, or the run is repeated on real NRC data (handoff-needs.md, M3). | Partly. The abstract (`paper/00-abstract.md` line 36) and the captions of Figures 2, 5 and 6 say synthetic; no one has checked every caption, and no real dataset has arrived. | None. |
| M4 | Viewer comparison in §4.3 with at least three rows tested; covers the tools SOW §3.2 names (handoff-needs.md, M4). | Partly. One row (the toolkit's viewer) is filled; seven rows still read "to test". | None. |
| M5 | Editorial pass: Q2 narrative consistent in §6.2 and §7.1, figures cited in order, no "will be reported in the next revision", real citations for the Duplex model and the National Building Code (NBC) (handoff-needs.md, M5). | Partly. References 6 (NBC 2020) and 18 (Duplex) exist. `paper/10-conclusion.md` line 29 still says "will be reported in the next revision". Appendix C's client configuration runs the server project by its old name, `Ara3D.Ifc.Mcp`, which the pinned toolkit no longer has (it is `BimOpenMcp.Ifc` under `deps/bim-open-data/src/mcp/`). | `paths` lists the Appendix C path as known missing (`checks/known-missing-paths.txt`); the rest none. |
| I1 | Write the Layer 2 reference as an `IfcDocumentReference` from `EnrichIfc` (handoff-needs.md, I1). | Partly. `IfcDocumentReferenceBuilder` exists in the toolkit at the pin; `poc/EnrichIfc/Program.cs` does not call it. | None. |
| I2 | A storey-of-element view, so Q2 counts 103 elements on Level 1 (handoff-needs.md, I2). | Met: `StoreyOfEntity` and the graph `nrc-storey-of-element` (Figure 10). | `toolkit-nrc` (`ModelGraphTests`); `poc` recomputes the Q2 storey means from the IFC by the same containment and aggregation walk. |
| I3 | Typed values through `sink.writePsets`, so the enrichment is one graph (handoff-needs.md, I3). | Met: `nrc-enrich-run`. | `toolkit-nrc` (`RollupGraphTests`). |
| I4 | An Information Delivery Specification (IDS) file for Layer 1, validated against the enriched model, with counts in §8.2 (handoff-needs.md, I4). | Not met. No `poc/nrc-analytics.ids`. | None. |
| I5 | Compliance verdicts for rule DC-W1 as a graph with a figure (handoff-needs.md, I5). | Met: `nrc-dc-w1-verdicts`, Figures 8 and 9, 8 pass and 6 fail. | `toolkit-nrc` (`ModelGraphTests`, `ShowcaseGraphTests`). |
| I6 | Mesh-accurate door clearance in the DC-Z1 zone test (handoff-needs.md, I6). | Not met. Paper §7 says the mesh path is not wired into the checker. | None. |
| I7 | Repeat the run on a second public model, `data/AC20-FZK-Haus.ifc` (handoff-needs.md, I7). | Not met. | None. |
| I8 | A Linux build of the MCP (Model Context Protocol) server, or a paragraph in §7 either way (handoff-needs.md, I8). | Partly. `paper/07-limitations.md` lines 76–77 say the stack is Windows-only; no Linux build. | None. |
| I9 | The toolkit test `BimSampleSeedingTests.EmptyStore_SeedsBimAndView3dSamples` passes on a machine with the private Snowdon sample (handoff-needs.md, I9). | Met at the pin: the test expects the Snowdon samples only when the model exists. | None in this repository (the test is in `BimOpenFlow.BimWorkflows.Tests`, which this CI does not run). |

## Toolkit workflow 6: reproduce the paper

| ID | Requirement and source | Status | Check |
|---|---|---|---|
| W6-1 | One command regenerates the paper's figures and transcripts (PROJECT.md, workflow 6). | Partly. `npm run nrc:walkthrough --prefix bimopenflow/web` in the toolkit does it by hand in about 4 minutes. The Snowdon half needs the private model and the LLM transcript needs a model key. | By hand, last run 2026-09-18 at toolkit `7e3192e` (`poc/results/walkthrough-index.md`). |
| W6-2 | A push that changes one of the paper's eight answers fails CI (PROJECT.md, workflow 6, Done). | Met from 2026-10-03. The toolkit's `CsvGraphTests` assert all eight (Q1 to Q8) over its copies of the analytics CSVs; `check_answers.py` asserts `expected_answers.json` against this repository's CSV for all eight, that the toolkit's copies equal this repository's files, and Q2, Q4 and Q6 from the property sets inside the enriched IFC. | `toolkit-nrc` and `poc`. |
| W6-3 | The walkthrough index lists every figure or the reason it was skipped (PROJECT.md, workflow 6, Done). | Partly. The copy here lists the ten Duplex figures; it has no Snowdon section and no skip reasons. | None. |
| W6-4 | The enriched IFC differs from the original only in the new property sets (PROJECT.md, workflow 6, Done). | Met. A fresh `EnrichIfc` run inserts one block of 3,766 property-set entities before `ENDSEC`, keeps every source byte, matches `psets_to_write.csv` value for value, and has the SHA-256 recorded in `poc/results/enrich-report.json`. | `poc` (`poc/check_enriched_ifc.py`). |
| W6-5 | The write-back happens from a Run (PROJECT.md, workflow 6). | Partly. The toolkit's `nrc-enrich-run` writes from a Run only inside its tests. The paper's file still comes from the `EnrichIfc` console program, and the two files differ: the toolkit's run writes 2,441 values, with the storey and building totals under their own names; the paper's file has 2,438. | `toolkit-nrc` (`RollupGraphTests.EnrichRun_WritesTheCommittedFileByteForByte`, for the toolkit's file only). |
| W6-6 | Every path this repository names into the toolkit exists at the pinned commit, so the documentation cannot drift from the code unnoticed (owner, 2026-10-03, for workflow 6's cost of failure). | Met, with five known exceptions listed in `checks/known-missing-paths.txt` (Appendix C's old server project path in four copies of the paper, and the old `AskAgent.cs` path in `paper/handoff-needs.md`). | `paths` (`checks/check_toolkit_paths.py`). |

## Summary

| Status | Count | IDs |
|---|---|---|
| Met | 13 | SOW-2, SOW-4, SOW-5, SOW-6, M1, M2, I2, I3, I5, I9, W6-2, W6-4, W6-6 |
| Partly | 10 | SOW-1, SOW-3, M3, M4, M5, I1, I8, W6-1, W6-3, W6-5 |
| Not met | 5 | SOW-7, SOW-8, I4, I6, I7 |

Rows with no check: SOW-1, SOW-6, SOW-7, SOW-8, M3, M4, I1, I4, I6, I7, I8, I9 (none in this
repository), W6-3; M5 is checked only for its Appendix C path.

## The pin moved to `v0.1` on 2026-10-04

The toolkit was split into separate repositories and `v0.1` is its first tagged tested set
(README of `bim-open-toolkit`, "Tested sets"). The toolkit has no nested submodules any more;
`node deps.mjs` fills `bim-open-toolkit/deps/` from `deps.json`. Every reference this
repository makes into the toolkit was moved the same day and `checks/check_toolkit_paths.py`
resolves `deps/<name>/...` through those pins: the byte-exact writer and the IFC MCP server
are under `deps/bim-open-data`, the dataflow host and node packs under `deps/bim-open-flow`, the 3D viewer under
`deps/bim-open-viewer`, and the bim-profile host is `src/studio/BimOpenFlow.Studio`. The NRC answer tests
are `tests/studio/BimOpenFlow.NrcWorkflows.Tests`.
