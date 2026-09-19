# Review of `condensed-paper.md`

Reviewer: fresh reader, 2026-09-19. Compared against `nrc-style-paper.md` (full paper), `storing-analytics-in-ifc.md`, and `nrc-style/p07-agent.md`.

## 1 Verdict

The condensed paper is fit to hand to a reader who will never see the full paper, subject to fixing the seven defects below, none of which needs more than a sentence. Its strongest quality is that the evidence survived the cut intact: every count, date, width, and verdict total in Sections 6.1 and 6.2 matches the full paper, and the storage defect found by the unattended run is stated in the abstract, the results, the limitations, and the conclusion. Its biggest weakness is Table 2, where the reader is told "seven of eight" and "four of eight" but cannot reproduce either count from the table, and where the Q5 row's expected values contradict its own "Match".

## 2 What to keep

- **Abstract, last sentence.** "The unattended run exposed one defect in the storage recommendation ... and that is the first correction to make." This is the paper's honesty in one line; it should stay in the abstract.
- **Section 2, "Three consequences shape everything that follows."** The only place the reader learns why property names are the schema, why one fact costs a whole parse, and why re-serialisation is fragile. Sections 3, 5, and the byte-exact writer all depend on it.
- **Section 3, the three layers and "Writing without disturbing the file."** The paragraph on deterministic `GlobalId` hashing and the entity diff is the single clearest statement of the write-back path in either paper.
- **Section 5, the four bulleted principles.** Each carries a concrete failure ("Without it the model made one call per element"). This is the substance of the query recommendation.
- **Section 5, "Compliance as a query."** The four-verdict scheme, with `InfoNotAvailable` for a null fact, is defined only here and Section 6.2 relies on it.
- **Section 6.1, the paragraph beginning "Three of the unattended misses share one cause."** The headline finding. The sentence "knowledge a prompt can carry but a file should not require" is the best line in the paper.
- **Section 6.2, ground truth paragraph.** The widths (2 at 1250, 6 at 864, 4 at 762, 2 at 813) predicting 8 pass and 6 fail before the checker ran is the reproducibility evidence.
- **Section 6.3.** Four sentences that explain why two unrelated-looking studies are one paper.
- **Section 7.** Kept every limitation of the full paper's Section 9 except typed write-back; the "favours it by construction" admission in the display paragraph should not be lost.
- **Figures 1 to 3.** One colouring, one verdict colouring, one pipeline diagram. The right three.

## 3 Where to improve

### Defects

1. **Table 1 (Section 3), row "Visualisation metadata | High | Low | Low | Low".** Neither the full paper's Table 4 nor the options brief's ranking table scores this mechanism; the row and its four scores are new. Remove the row, or add "not scored in the brief" and drop the scores.
2. **Table 2, Q5.** Expected reads "Wall 22,854.1, Floor 5,593.5" (per analytics category) while hand-driven reads "Match, grouped by IFC class". The full paper's Table 8 shows the hand-driven expectation was per class (walls 17,547.4). As written the row says a class total matched a category total. Fix: give both expectations, or change hand-driven to "Match against the per-class expectation (walls 17,547.4)".
3. **Table 2, match counts.** Only Q1, Q2, and Q6 say "Match" in the unattended column, yet the text claims four of eight; Q4 is counted as a match in the full paper (Table 9, "Yes"). Same for the hand-driven Q4. Write "Match: all four listed, question returned" so the reader can count.
4. **Section 5, second surface.** "whose tools are the same four graph operations that back the web editor" is wrong; the full paper (7.4, Annex C.2) lists six tools (`describeDatabase`, `getNodeCatalog`, `editGraph`, `evaluate`, `getResult`, `createRun`), of which `editGraph` applies the four operations. Section 2 of the condensed paper says it correctly ("back the ... MCP tools").
5. **Section 4, viewer paragraph.** "All support colouring by property" contradicts the full Table 5, where FreeCAD NativeIFC is "Partial", and "requires scripting in every case but the toolkit's" contradicts FZKViewer's "No". Write "All but FreeCAD (partial) colour by property; FZKViewer cannot colour from an external table and the others need a script or plug-in."
6. **Section 3, Layer 2 column list.** Ten columns are given; the full paper (5.4) gives twelve, including `MetricName` and `Confidence`. Either restore the two or say "including".
7. **Section 3, last sentence.** "The first, third, and fifth measures are implemented and tested; the IDS remains future work." The full paper adds "Measure 4 is a document", and the condensed Section 7 says the dictionary is not implemented. Add the clause so the reader is not left to infer the second and fourth.

### Design notes

- **Abstract, "56 verdicts that matched independently derived ground truth door by door".** The ground truth predicts DC-W1 only (Section 6.2). The full paper's body says "DC-W1 matches the ground truth exactly". Say "with DC-W1 matching ground truth door by door".
- **Abstract** drops the match counts (7 of 8, 4 of 8) that the full executive summary states. A reader of the abstract alone learns the questions were "answered", not how well.
- **Section 5, "A typical answer is two calls."** The hand-driven session used one or two; the unattended run averaged over four (35 calls over 8 questions, 3 to 11 each). Say "one to two in the hand-driven session".
- **Section 5, dataflow figures.** "ten correct graphs and two honest non-answers" compresses "ten correct graphs, one honest answer without a graph, and one correctly empty graph with an explanation", and drops the mid-sized result (eleven and one). Restore one clause.
- **"Twelve mechanisms" against an eleven-row table.** The full paper has the same gap (ten rows). Add "library and classification references are one row" to the caption.
- **Figure 2 caption** uses `check.rule` a section before it is defined. Either move the definition forward or write "a rule node" here.
- **Section 8, near term** lists four items; the full 10.1 lists five. The dropped one (typed values through `sink.writePsets`) is also missing from the limitations. Either add one sentence or accept the omission knowingly.
- **Section 4, "a real building of 456,598 instances".** The full paper says it is a private sample; say so, since the reader cannot obtain it.
- **Undefined terms:** STEP (used from Section 2 with no expansion), "text views" (Sections 5 and 6, never explained), and reference [29], listed but never cited. FZK-Haus is named without [19].
- **Section 2, MCP paragraph** and **Section 5, opening** both say the file exceeds the context window and the model cannot read STEP. Keep the Section 5 version and cut two sentences from Section 2.

## 4 Fidelity check

Every number and date checked: 38,898; 664; 2,438; 3,766; 218; 14; 61; 8/6; 4/2/8; 0/0/0/14; 14/0/0/0; 93 of 103; 40.50 vs 40.56; 37,196.2; 54.0; 49,451.2; 48,696.8; 35 calls; 29 tools; 456,598; 850 mm; 25 mm; `71790a7`; 2026-08-04, -08-05, -09-17, -09-18, -09-19. All match.

| Item | Condensed says | Full paper says |
|---|---|---|
| Visualisation metadata scores | High, Low, Low, Low | Not scored (Table 4 has no such row) |
| Q5 hand-driven expectation | Wall 22,854.1 (category) | Walls 17,547.4 (class), Table 8 |
| Layer 2 columns | 10 | 12 |
| Dataflow MCP tools | "four graph operations" | Six tools; `editGraph` carries the four operations |
| Viewers colouring by property | All | FreeCAD "Partial" |
| Dataflow results | 10 correct, 2 non-answers | 10 correct, 1 no-graph, 1 correctly empty; plus 11 and 1 on mid-sized |
| Near-term items | 4 | 5 |

Headline findings dropped: the mechanical replay of Q1, Q5, Q7, Q8 over stdio matching on 2026-09-18 (the only language-model-free check of the tool surface); the test-run line "seven tests passed in approximately four seconds, verified twice"; the token cost of the unattended run (221,968 input, 30,144 output), which is the only cost figure in either paper.

Hedges the condensed paper loosens: the abstract's "56 verdicts that matched ... ground truth" (full: DC-W1 matched); "a typical answer is two calls" (full: illustrative exchange, three calls, "not measured results").

## 5 Length

At 5,240 words it renders to 11 pages. Three cuts, in order:

1. **Section 8, "Knowledge graphs and world models" and "Federated collections" (about 260 words).** Reduce to one paragraph of four sentences. Lost: the argument for RDF export rather than RDF store, and the identifier problem. Both are future work the statement of work asked about, so keep one sentence each.
2. **Section 4, second paragraph and the viewer paragraph (about 200 words).** Merge the graph description into the Figure 1 caption and cut the viewer name list to "eight viewers [23]". Lost: the named shortlist, recoverable from the reference.
3. **Section 6.1, first paragraph (about 120 words).** The procedure repeats what Section 3 established about the writer. Keep the enrichment counts and "expected answers were computed from the CSV alone"; drop the rest. Lost: nothing the reader has not already been told.

Together these recover roughly 600 words, about one page.
