# Review of `paper-v2.md` (version 2, 2026-10-04)

Reviewer: a fresh reader who did not write the paper. Every number below was checked against the files named, on the toolkit submodule at `v0.1` (`59aeb6d`).

## 1 Verdict

Fit to send after one editing pass: the evidence is real, committed, and almost every figure in the text matches it, but the paper has a handful of contradictions and overclaims a client reviewer would catch. Its strongest quality is the control experiment in Section 6.2, where the same model and guide run on both files and the version 1 misses reappear exactly where the paper predicts (Q1 at three times the total, Q3 ranking the building and storeys). Its biggest weakness is the sentence "Every number in this paper is asserted by a test", which is false for the IFC-Bench score, the Claude match counts, the token counts, and the cost, and which the conclusion repeats.

## 2 Fidelity check

Confirmed, no action needed: the scorer rerun reproduces `scores.md` byte for byte; model, effort, and toolkit commit in every transcript header; all Table 4 cells, the Q7 values (5,821.0; 1,838.5; 2,059.1), the control quote in old-run2, 111,589 over 223 entities, the containers ranked in Q3 and listed in Q5; 2,863,052 input and 65,279 output tokens, turns 42 to 51, both input ranges; Table 3's counts on both sides (`enrich-report.json`, toolkit `samples/nrc/README.md`); 15 dictionary rows and `NRC-metrics-0.2`; 70 tests (32 `[Test]`, 4 `[TestCase]`, 2 `[TestCaseSource]` over 17 graphs); the 37,196.2 and byte-for-byte assertions in `RollupGraphTests.cs`; 29 IFC MCP tools with four hidden in `IfcAskRunner.cs`; every IFC-Bench figure in Table 5 and 6.3 against `TKT-145`, including that the three fixes (`95db8e2`) sit inside the `v0.1` pin of bim-open-data; the three figure files; seven MCP servers; the door study numbers; the `v0.1` date.

Mismatches:

| Claim | Paper says | Evidence says | File |
|---|---|---|---|
| Table 1 row count | "Twelve mechanisms" | Table has 10 rows. Brief mechanisms 7 and 8 (library references, classification/bsDD) are one row; mechanism 11 (visualisation-oriented metadata) is absent. | `storing-analytics-in-ifc.md` headings 1 to 12 |
| Size of the tested set | Section 1.1 and 6.5 third bullet: "six repositories" | Section 6.5 first bullet and the toolkit README: "eight other repositories"; `deps.json` pins eight (gratify, ara3d-sdk, ara3d-dataflow, schema, data, flow, viewer, notebook). Section 2 names five plus the toolkit. | `bim-open-toolkit/deps.json`, `README.md` "Tested sets" |
| "Every number in this paper is asserted by a test" (abstract, Section 9) | asserted by tests in two repositories | IFC-Bench 62 of 100, $6.79, 46 min, the 7/7/7 and 5/6/4 Claude counts, token totals, and 456,598 instances are recorded, not asserted. `REQUIREMENTS.md` SOW-3 and M2 mark the Claude runs "By hand". | `REQUIREMENTS.md` rows SOW-3, M2 |
| IFC-Bench defects "all in the data layer and none in the agent" (6.3) | three data-layer defects | Defect 3 is the agent's guide ("The guide let the model add"). The closing sentence of 6.3 repeats "all in how the file was read into tables". | `TKT-145` note of 2026-10-04 |
| IFC-Bench rerun "four correct" (6.3) | stated without qualifier | "Reviewed by the agent that made the fixes, not the owner." | `TKT-145` |
| Proposal progress (Section 8) | "lists eight pieces; four have landed (contract and rollup, test-kit join template, deterministic answer tests, external benchmark)" | The proposal's eight are P1 to P8. The answer tests predate it (it cites TKT-19 and TKT-32 as existing); the external benchmark is TKT-145, not one of the eight; P4 asked for 16 questions and five runs, the paper has 8 and three; P5's large-model timing is undone. Only P1 is complete, P5 in part. | `docs/proposals/nrc-deliverables.md` |
| IFC-Bench coverage | abstract and 1.1: "100 questions over 22 public models"; 6.3: "22 building models", then "16 of the 22 projects" | Dataset: 22 projects. Subset: "100 questions over 22 models of at most 80 MB" from the 16 eligible projects. "Model" and "project" are never defined, and the abstract reads as if all 22 projects were used. | `TKT-145` |
| Quotation in 6.2 | "all 223 building elements that carry it" in quotation marks | old-run2: "across all 223 building elements that carry this property"; old-run3: "... that carry this metric". A paraphrase, not a quote. | `old-run2.json`, `old-run3.json` Q1 |
| Path check "fails when one does not exist" (6.5) | no exceptions mentioned | Four tolerated exceptions (Appendix C's old `src/Ara3D.Ifc.Mcp` in four version 1 copies). | `checks/known-missing-paths.txt`, `REQUIREMENTS.md` W6-6 |
| "Table 2 shows it in full" (3.4) | full dictionary | `ValueType`, `Description`, `Decimals` columns are dropped; derivation 2 then refers to `Decimals`, which the reader cannot see. | `nrc-metrics.csv` |
| Control Q7 "reported only when the agent lands on the IFCROOF entity, as the control did once" (6.2) | once | old-run3 also landed on `IFCROOF` (id 22475), said it carries no value, then gave the storey rollup (Partial). The control reached the entity twice and led with absence once. | `old-run3.json` Q7 |
| Table 3 "Aggregates supplied by: the data generator" | implies totals were inputs | True as stated, but `generate_synthetic_analytics.py` lines 153 to 175 computed them from element values. The version 2 gain is where the computation lives and that a test asserts it, not that totals became derived. | `poc/generate_synthetic_analytics.py` |

Eleven mismatches, of which the first seven need a text change; the last four are precision.

## 3 Defects and design notes

**Defects (must fix)**

1. Abstract, last sentence, and Section 9, last sentence. "Every number ... is asserted by a test." Replace with what is true: the eight answers, the figure counts, the enrichment bytes, and the DC-W1 verdicts are asserted; the model runs and the benchmark are recorded with transcripts and a committed scorer.
2. Section 1.1 contribution 4, Section 6.5 bullet 3. "six repositories". Use "the toolkit and its eight pinned dependencies" everywhere, or define the six and say which two are left out.
3. Table 1 and Section 3.2. Ten rows for "twelve mechanisms". Add the two missing rows or write "ten rows; two pairs are merged and one mechanism is omitted as display-only".
4. Section 6.3, sentence before the list and the second conclusion. "none in the agent" and "all in how the file was read" contradict item 3. Say "two in the data layer and one in the guide", and let the conclusion say the guide fix is the rule Section 5.2 now states.
5. Section 6.3, rerun paragraph. Add "judged by the same evaluating agent, not yet by the author".
6. Section 8, first paragraph. Replace "four have landed" with the honest state: P1 done, the P5 template graph done, P4 measured at three runs of eight questions instead of five of sixteen, the benchmark outside the proposal.
7. Section 6.3 and abstract. Define "project" and "model" once, and say the 100 questions ran over models from the 16 eligible projects.
8. Section 6.2. Either quote old-run2 verbatim or drop the quotation marks.
9. Section 6.5 bullet 3. Add "with four recorded exceptions in version 1 files that await the editorial pass".
10. Section 3.4. "Table 2 shows the seven columns the derivations use; the file has three more (`ValueType`, `Description`, `Decimals`)."
11. Table 4, Q2, hand-driven "Miss" has no explanation in version 2 (version 1 gave it: the relation walk reached 93 of 103 Level 1 elements). One clause in 6.2.
12. Undefined terms a client reader will meet: "turn", "effort" ("medium effort"), "DigitalHub" (6.3), "stratified". One parenthesis each.

**Design notes (may fix)**

1. Abstract, third paragraph: one 130-word sentence carrying nine numbers. Split into three.
2. Section 1.1 bullet 3: "several times each" is three. Say three.
3. Table 3, "Aggregates supplied by" row: "computed by a Python script and passed to the writer as rows" against "computed by the `nrc-rollup` graph inside the run and asserted by a test". That is the real difference.
4. Section 5.3's twelve-request figure is unchanged from version 1 and cites no evidence file. Cite the transcript or cut the numbers and keep the design.
5. Section 2, last paragraph, is a product catalogue of five repositories plus four engine operations. The paper needs two sentences here; the rest belongs to reference [8].
6. Sentences that read as generated rather than written: "That is the property version 1 asked for and version 2 has"; "unchanged and stronger" (3.5); "worth restating, because the fix is a design rule and not a rename" (3.4); the final paragraph of Section 9, carried over from version 1. Each can lose its flourish.
7. Section 6.2, Q7: the paper argues the expected answer is arguably wrong and the slab answer is better, then headlines 7 of 8 as if the miss were a defect. Say in the abstract "7 of 8, the eighth a question whose expected answer this paper disputes", or rescore Q7 and report 8 of 8 with the old rule in a footnote. Do not leave both readings standing.
8. Section 8 is 1,000 words of roadmap in eight prose blocks. A table (piece, done-when, depends on) halves it.
9. Figures 1 and 2 are version 1 captures of a file the paper has replaced. One walkthrough run regenerates them and removes a limitation from Section 7.

## 4 Contributions

Contribution 2 (the model behind a small typed tool surface, measured twice) is the strongest and fully supported: three identical 7 of 8 runs on the new file against 5, 6, 4 on the old, and 62 of 100 on a question set written by someone else, with the 29 wrong answers read one by one.

Contribution 1 (the comparison and the contract) is half new. The contract is well supported by `nrc-metrics.csv`, the two graphs, and the two tests. The twelve-mechanism comparison is version 1's, and its table is short two rows.

Contribution 3 (byte-exact, reproducible write-back "by which analytics, verdicts, and human overrides may be added") overstates by one clause. Analytics are written by the dataflow run and asserted byte for byte. Verdicts and overrides were written by the August checker (`Ara3D_Compliance`, Section 6.4), not by the run. Say so.

Contribution 4 (the reproducibility apparatus) is real and is the paper's distinctive move, but its own description overclaims (defects 1, 2, 9).

Contribution 5 (the roadmap) is not a contribution; it is Section 8. Drop it from the list, or fold it into 4 as "and a costed list of what remains".

Under-sold: the control experiment itself. Running the same model and guide over both files, with the misses falling exactly where Section 3.4 predicts, and Q1 showing that the toolkit-side mitigation (`StoreyOfElement`) never covered a sum that does not group by storey, is a cleaner demonstration of the storage defect than anything in version 1. It deserves a sentence in Section 1.1 and the abstract rather than a parenthesis.

## 5 What to keep

- Section 3.4, the four derivations and "Nothing in the input supplies a total; a total is something a graph computes." This is the paper's thesis in one line and it is tested (`RollupGraphTests.cs` lines 82 and 206).
- Table 2 (the dictionary). It is the artefact; the client can diff it against the CSV.
- Table 3. The only place the two enrichments sit side by side; fix the aggregates row and keep the rest.
- Table 4 with the rule in the second column. A reader can see what "Match" meant for each question without opening the scorer.
- Section 6.2, paragraphs on the version 1 control (111,589 over 223 entities; building and storeys ranked as elements). Concrete, quoted from transcripts, and the best evidence for the contract.
- Section 6.3, the three defects and the first conclusion ("an external question set finds defects an internal one cannot, because the internal set is written by the people who know where the data is").
- Section 5.1, the fifth principle ("The file tells the agent how to read it"), and Section 7, "Of the measurements", which names the agent-judged verdicts and the one-model-family limit without hedging.
