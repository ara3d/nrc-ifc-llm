# Requirements

One table of what this repository has to deliver, where each requirement comes from, whether
it is met today, and what checks it. Status was assessed on 2026-10-03 against this
repository's `main` and the BIM Open Toolkit submodule pinned at tag `v0.2` (`bf1e4a9`); the pin moved from `v0.1` (`59aeb6d`) on 2026-10-17 and from `34499e3` on 2026-10-04.

Sources:

- **SOW**: [statement-of-work.md](statement-of-work.md), the contract with the National
  Research Council Canada (NRC).
- **M1–M5, I1–I9**: `handoff-needs.md` in the paper folder (outside the repository), the minimal (M) and
  ideal (I) items for the paper.
- **W6**: workflow 6 of the toolkit's brief, `PROJECT.md` in `bim-open-toolkit` at the pin,
  "Reproduce the paper, including the write-back, with one command".

Checks named `paths`, `poc` and `toolkit-nrc` are jobs of
[.github/workflows/check.yml](.github/workflows/check.yml), which runs on every push and pull
request. "None" means nothing checks the requirement, by machine or by a recorded hand run.

## Statement of work

| ID | Requirement and source | Status | Check |
|---|---|---|---|
| SOW-1 | An options analysis of storing and displaying analytics at component, zone, storey and building level, with a comparison matrix and recommendations (SOW §2.1, §2.2, D1, §6 first criterion). | Partly. A standalone brief exists, written 2026-10-17 and not yet reviewed by NRC: `d1-options-brief.md` and its PDF (11 pages) in the paper folder outside this repository (`C:\Users\cdigg\nrc\paper`). It covers storage and display at component, zone, storey and building level with two matrices and numbered recommendations; the zone level is a named mechanism in the brief and a demonstration on the Duplex (SOW-10). Met once NRC accepts it. | None. |
| SOW-2 | The proof of concept includes an IFC model enriched with analytics through the recommended storage approach (SOW §3.3, D2). | Met. `poc/data/duplex-enriched.ifc`: 664 property sets and 2,438 values written into `IFC-Test-Kit/duplex.ifc` by `poc/EnrichIfc`. | `poc` (see W6-4). |
| SOW-3 | An agent based on a large language model (LLM) answers natural-language questions about the stored carbon, energy and other analytics at component, zone and building level (SOW §3.3, D2, §6 second criterion). | Met. Claude Haiku 4.5 through the Claude Code command line, unattended, answered 7, 9 and 7 of 9 questions in three runs over the toolkit's `v0.2` `samples/nrc/duplex-enriched.ifc` (`NRC_*` set names, zones), against 4, 4 and 5 of 9 over the version 1 control file (`poc/results/unattended/2026-10-17/`, README there). The misses over the `v0.2` file are Q5 (class totals summarised, not all 14 given) and Q7 (container elements listed beside the roof) in the runs that miss. The 2026-10-04 runs of the eight earlier questions (7, 7, 7 of 8 and 5, 6, 4 of 8) are kept as history. Earlier: `gpt-5` 4 of 8 (2026-09-18), hand-chosen tool calls 7 of 8. | By hand, last run 2026-10-17 (`poc/results/unattended/2026-10-17/`, scored by `poc/score_unattended.py`). `poc` re-reads the recorded gpt-5 Q2, Q4 and Q6 answers; it calls no model. |
| SOW-10 | Storage and display at zone level are demonstrated, not only described (SOW §2.1, D1). | Met on the Duplex. `nrc-zones.csv` groups the model's own 20 conditioned spaces into four zones, written back as `IfcZone` groups with an `NRC_ZoneSummary` set each (toolkit `v0.2`); the ninth question asks which zone has the highest energy use intensity (Unit B Level 1, 78.04 kWh/m2/yr) and the agent answered it in 3 of 3 runs. The zones are synthetic, made from the room numbers; the KIT validation model was not tried. | `poc` (`check_answers.py`: Q9 computed from the zone tables and read back from the zone sets in the IFC) and `toolkit-nrc` (`CsvGraphTests.Q9_ZoneEnergyUseIntensity`). |
| SOW-4 | A lightweight visualisation colours the model by analytics value (SOW §3.3, D2). | Met. Figures 5 to 8 in the paper's `figures/` folder. | By hand, last run 2026-09-18 (`poc/results/walkthrough-index.md`); `toolkit-nrc` asserts the row and colour counts behind each Duplex figure (`FigureGraphTests`). |
| SOW-5 | The proof-of-concept package carries its source code and documentation (SOW D2). | Met. `poc/README.md` lists every file and the commands that regenerate them. | `paths` (every toolkit path the documentation names exists at the pin) and `poc` (the documented commands run). |
| SOW-6 | The paper covers storage, display, the role of LLM and agent layers, proof-of-concept results, knowledge graphs and world-model substrates as extensions, and a roadmap for an open bidirectional viewer (SOW §3.4). | Met. Paper §3, §4, §5, §6, §8.3 and §8.4, §9. | None. |
| SOW-7 | The paper passes the client's editorial review (SOW D3, §6 third criterion). | Not met. No review is recorded; the editorial pass M5 is still open. | None. |
| SOW-8 | A final presentation and handover to the client team (SOW D4, §6 fourth criterion). | Not met. Nothing in the repository records one. | None. |
| SOW-9 | The proof-of-concept code is in a public repository under an OSI-approved open-source licence selected by the NRC, with the NRC as copyright holder (SOW §4 D2, §5). | Partly: LICENSE placeholder, NRC's choice pending. The repository is public (confirmed 2026-10-17). `LICENSE` proposes MIT with the NRC as copyright holder and says the NRC selects the licence; the README section "Deliverable D2: what is NRC-owned and where" maps the three D2 items to files and asks the NRC the licence question. Met once the NRC chooses and `LICENSE` is replaced or confirmed. | None automated; the file is `LICENSE`. |

## Handoff items for the paper

| ID | Requirement and source | Status | Check |
|---|---|---|---|
| M1 | A 3D colour-coded figure of the public Duplex model (handoff-needs.md, M1). | Met 2026-09-18: Figures 5 to 10 in the paper's `figures/` folder, cited in §4. | Same as SOW-4. |
| M2 | An unattended LLM run of the paper's questions, with model name and per-question match in §6.2 (handoff-needs.md, M2). | Met: `gpt-5`, 2026-09-18, toolkit `66df499` (4 of 8); Claude Haiku 4.5, 2026-10-04, toolkit `v0.1`, three runs on each file, per-question table in paper v2 Table 4; Claude Haiku 4.5, 2026-10-17, toolkit `v0.2`, nine questions, three runs on each file. | By hand, last run 2026-10-17; `poc` checks the recorded gpt-5 Q2, Q4 and Q6 answers. |
| M3 | Every number in the abstract and every figure caption is labelled synthetic, or the run is repeated on real NRC data (handoff-needs.md, M3). | Partly. The abstract (`00-abstract.md` line 36) and the captions of Figures 2, 5 and 6 say synthetic; no one has checked every caption, and no real dataset has arrived. | None. |
| M4 | Viewer comparison in §4.3 with at least three rows tested; covers the tools SOW §3.2 names (handoff-needs.md, M4). | Partly. One row (the toolkit's viewer) is filled; seven rows still read "to test". | None. |
| M5 | Editorial pass: Q2 narrative consistent in §6.2 and §7.1, figures cited in order, no "will be reported in the next revision", real citations for the Duplex model and the National Building Code (NBC) (handoff-needs.md, M5). | Partly. References 6 (NBC 2020) and 18 (Duplex) exist. `10-conclusion.md` line 29 still says "will be reported in the next revision". Appendix C's client configuration runs the server project by its old name, `Ara3D.Ifc.Mcp`, which the pinned toolkit no longer has (it is `BimOpenMcp.Ifc` under `deps/bim-open-data/src/mcp/`). | None (the paper is outside the repository, so `paths` no longer scans it). |
| I1 | Write the Layer 2 reference as an `IfcDocumentReference` (handoff-needs.md, I1). | Met for the toolkit's file. Since `v0.2`, the Run `nrc-enrich-run` (`sink.writePsets` with `documentPath`) writes an `IfcDocumentReference` and `IfcRelAssociatesDocument` on the project naming `nrc_analytics_long.csv` with its format, SHA-256 and join key `GlobalId`. `poc/EnrichIfc` (the version 1 control) still does not. | `toolkit-nrc` (`RollupGraphTests.Enriched_CarriesADocumentReferenceToTheLongTable`). |
| I2 | A storey-of-element view, so Q2 counts 103 elements on Level 1 (handoff-needs.md, I2). | Met: `StoreyOfEntity` and the graph `nrc-storey-of-element` (Figure 10). | `toolkit-nrc` (`ModelGraphTests`); `poc` recomputes the Q2 storey means from the IFC by the same containment and aggregation walk. |
| I3 | Typed values through `sink.writePsets`, so the enrichment is one graph (handoff-needs.md, I3). | Met: `nrc-enrich-run`. | `toolkit-nrc` (`RollupGraphTests`). |
| I4 | An Information Delivery Specification (IDS) file for Layer 1, validated against the enriched model, with counts in §8.2 (handoff-needs.md, I4). | Partly. The toolkit at `v0.2` generates `samples/nrc/ids/nrc-analytics.ids` (two specifications, IDS-OC and IDS-EC, over the 14 analysed classes) from `samples/nrc/nrc-metrics.csv` by `scripts/nrc-ids.mjs`; its own evaluator over the enriched file gives IDS-OC 218 pass and IDS-EC 217 pass, 1 fail (the roof). No independent IDS tool has validated the analytics IDS; the ifctester parity test covers the door rule only and skips when ifctester is absent. | `toolkit-nrc`: `IdsFilesTests.TheGeneratedIds_MatchesTheMetricDictionary`; the golden `tests/studio/BimOpenFlow.SampleFlows.Tests/golden/bim/check-ids-carbon-psets.txt` in the toolkit's own CI. |
| I5 | Compliance verdicts for rule DC-W1 as a graph with a figure (handoff-needs.md, I5). | Met: `nrc-dc-w1-verdicts`, Figures 8 and 9, 8 pass and 6 fail. | `toolkit-nrc` (`ModelGraphTests`, `ShowcaseGraphTests`). |
| I6 | Mesh-accurate door clearance in the DC-Z1 zone test (handoff-needs.md, I6). | Not met. Paper §7 says the mesh path is not wired into the checker. | None. |
| I7 | Repeat the run on a second public model, `data/AC20-FZK-Haus.ifc` (handoff-needs.md, I7). | Not met. | None. |
| I8 | A Linux build of the MCP (Model Context Protocol) server, or a paragraph in §7 either way (handoff-needs.md, I8). | Partly. `07-limitations.md` lines 76–77 say the stack is Windows-only; no Linux build. | None. |
| I9 | The toolkit test `BimSampleSeedingTests.EmptyStore_SeedsBimAndView3dSamples` passes on a machine with the private Snowdon sample (handoff-needs.md, I9). | Met at the pin: the test expects the Snowdon samples only when the model exists. | None in this repository (the test is in `BimOpenFlow.BimWorkflows.Tests`, which this CI does not run). |

## Toolkit workflow 6: reproduce the paper

| ID | Requirement and source | Status | Check |
|---|---|---|---|
| W6-1 | One command regenerates the paper's figures and transcripts (PROJECT.md, workflow 6). | Partly. `npm run nrc:walkthrough --prefix bimopenflow/web` in the toolkit does it by hand in about 4 minutes. The Snowdon half needs the private model and the LLM transcript needs a model key. | By hand, last run 2026-09-18 at toolkit `7e3192e` (`poc/results/walkthrough-index.md`). |
| W6-2 | A push that changes one of the paper's nine answers fails CI (PROJECT.md, workflow 6, Done). | Met from 2026-10-03, nine questions from 2026-10-17. The toolkit's `CsvGraphTests` assert Q1 to Q8 and its zone graph test Q9 over its copies of the analytics CSVs; `check_answers.py` asserts `expected_answers.json` against this repository's CSV and the toolkit's zone tables for all nine, that the toolkit's copies equal this repository's files, and Q2, Q4 and Q6 from the property sets inside the version 1 control file and the toolkit's file, plus Q7 and Q9 from the latter. | `toolkit-nrc` and `poc`. |
| W6-3 | The walkthrough index lists every figure or the reason it was skipped (PROJECT.md, workflow 6, Done). | Partly. The copy here lists the ten Duplex figures; it has no Snowdon section and no skip reasons. | None. |
| W6-4 | The enriched IFC differs from the original only in the new property sets (PROJECT.md, workflow 6, Done). | Met. A fresh `EnrichIfc` run inserts one block of 3,766 property-set entities before `ENDSEC`, keeps every source byte, matches `psets_to_write.csv` value for value, and has the SHA-256 recorded in `poc/results/enrich-report.json`. | `poc` (`poc/check_enriched_ifc.py`). |
| W6-5 | The write-back happens from a Run (PROJECT.md, workflow 6). | Met. The toolkit's `samples/nrc/duplex-enriched.ifc` at `v0.2` (2,469 values in 663 sets on 228 entities, `NRC_*` names, four zones, a document reference to the long table; written by a Run of `nrc-enrich-run`) and is used for the Claude runs of 2026-10-17 (paper v2 cited the 659-set file of `v0.1`). `poc/data/duplex-enriched.ifc` (2,438 values, `EnrichIfc` console program) is kept as the version 1 file and the control. | `toolkit-nrc` (`RollupGraphTests.EnrichRun_WritesTheCommittedFileByteForByte`). |
| W6-6 | Every path this repository names into the toolkit exists at the pinned commit, so the documentation cannot drift from the code unnoticed (owner, 2026-10-03, for workflow 6's cost of failure). | Met. The five former exceptions in `checks/known-missing-paths.txt` were all in the paper, which left the repository on 2026-10-15. | `paths` (`checks/check_toolkit_paths.py`). |

## Summary

| Status | Count | IDs |
|---|---|---|
| Met | 17 | SOW-2, SOW-3, SOW-4, SOW-5, SOW-6, SOW-10, M1, M2, I1, I2, I3, I5, I9, W6-2, W6-4, W6-5, W6-6 |
| Partly | 9 | SOW-1, SOW-9, M3, M4, M5, I4, I8, W6-1, W6-3 |
| Not met | 4 | SOW-7, SOW-8, I6, I7 |

Rows with no check: SOW-1, SOW-6, SOW-7, SOW-8, SOW-9, M3, M4, I6, I7, I8, I9 (none in this
repository), W6-3; M5 is checked only for its Appendix C path.

## The pin moved to `v0.2` on 2026-10-17

`v0.2` renamed the NRC property sets from `Pset_NRC*` to `NRC_*`, reworded Q4, Q5 and Q7, added the zone level and Q9, and made the enriched sample carry an `IfcDocumentReference` to the long table. `deps.json` of the toolkit pins bim-open-data `d5e45d6` and bim-open-flow `71dbc44`; the NRC test project passes 108 of 108.

## The pin moved to `v0.1` on 2026-10-04

The toolkit was split into separate repositories and `v0.1` is its first tagged tested set
(README of `bim-open-toolkit`, "Tested sets"). The toolkit has no nested submodules any more;
`node deps.mjs` fills `bim-open-toolkit/deps/` from `deps.json`. Every reference this
repository makes into the toolkit was moved the same day and `checks/check_toolkit_paths.py`
resolves `deps/<name>/...` through those pins: the byte-exact writer and the IFC MCP server
are under `deps/bim-open-data`, the dataflow host and node packs under `deps/bim-open-flow`, the 3D viewer under
`deps/bim-open-viewer`, and the bim-profile host is `src/studio/BimOpenFlow.Studio`. The NRC answer tests
are `tests/studio/BimOpenFlow.NrcWorkflows.Tests`.
