# Unattended runs of the nine questions, 2026-10-17

Six runs of Claude over the BIM Open Toolkit's IFC MCP server, scored by `python poc/score_unattended.py`. The analytics values in the model are synthetic.

## Conditions

| Item | Value |
|---|---|
| Date | 2026-10-17, runs between 18:08 and 18:38 (Eastern time) |
| Model and effort | Claude Haiku 4.5 (`claude-haiku-4-5-20251001`), medium effort, through the Claude Code command line; no API account |
| Runner | `bimopenmcp-ifc-ask` from toolkit tag `v0.2`, commit `bf1e4a92` (`bim-open-toolkit` submodule); one fresh conversation per question, every tool call recorded |
| Questions | `bim-open-toolkit/samples/nrc/questions.txt`, nine questions, SHA-256 `aa183ce48ee8e1ae1d85105dcdd3b54181380a252dd29573fe739645415c2750` |
| `new-run1` to `new-run3` | the toolkit's `samples/nrc/duplex-enriched.ifc` at `v0.2`: `NRC_*` set names, four `IfcZone` groups, an `IfcDocumentReference` to the long table; SHA-256 `c263e08ca0ddce05d4fa34dd8e9897edc93f12c8621e61c232d7fd8138600078`; 663 property sets, 2,469 values on 228 entities |
| `old-run1` to `old-run3` | the control, `poc/data/duplex-enriched.ifc`, version 1: `Pset_NRC*` names, summaries stored under the element names, no zones; SHA-256 `c72447cbd5329e224e851e0550d89cbefc20a69e22d18b621e1be80dadac22c8`; 664 property sets, 2,438 values |
| Scorer | `poc/score_unattended.py` over `poc/results/expected_answers.json`; one deterministic rule per question, printed in the table |

Run order. `new-run2`, `new-run3`, `old-run1` and `old-run3` ran in pairs, one new and one old at a time. `new-run1` and `old-run2` were made again: the first `new-run1`, run in the first pair beside `old-run1`, showed `Pset_NRC*` names in its tool results although it opened the new file, so it was discarded (suspected cause: the two servers share a derived-file store under the system temp folder and both name their copy `duplex-enriched`; not yet confirmed), and the first `old-run2` was cut short when a stray command on the machine ended one of the two processes. Both were repeated alone, one after the other. The other four runs contain no name from the other file.

## Scores

Verdicts: Match, Partial, Miss. Q4, Q5 and Q7 are the reworded questions; Q9 is new. The old file has no zones, so Q9 cannot be answered from it: its runs correctly say so and the scorer calls that a Miss.

| # | Rule | new-run1 | new-run2 | new-run3 | old-run1 | old-run2 | old-run3 | Matches |
|---|---|---|---|---|---|---|---|---|
| Q1 | states 37196.2 | Match | Match | Match | Miss | Miss | Miss | 3 of 6 |
| Q2 | Level 2 named higher, means 40.56 and 40.50 stated | Match | Match | Match | Match | Match | Match | 6 of 6 |
| Q3 | the five values 412.0, 410.8, 402.0, 399.7, 398.6; no container ranked | Match | Match | Match | Miss | Miss | Miss | 3 of 6 |
| Q4 | 54.0 stated for the door with the given GlobalId | Match | Match | Match | Match | Match | Match | 6 of 6 |
| Q5 | all 14 per-class totals stated (whole numbers accepted); container rows not listed | Miss | Match | Miss | Miss | Miss | Miss | 1 of 6 |
| Q6 | run-2026-09-17-01 and 2026-09-17 stated | Match | Match | Match | Match | Match | Match | 6 of 6 |
| Q7 | the one IfcRoof (0jf0rYHfX3RAB3bSIRjmxl) named; another element, project, storey or zone listed is a Partial | Partial | Match | Miss | Partial | Partial | Match | 2 of 6 |
| Q8 | 49,451.2; 48,696.8; 11,761.3; 5,821.0 stated (doubles are the aggregate defect) | Match | Match | Match | Match | Match | Match | 6 of 6 |
| Q9 | Unit B Level 1 named with 78.04 kWh/m2/yr | Match | Match | Match | Miss | Miss | Miss | 3 of 6 |
| **Matches** | | 7 | 9 | 7 | 4 | 4 | 5 | |

| Run | Turns | Input tokens | Output tokens |
|---|---|---|---|
| new-run1 | 45 | 484,421 | 11,263 |
| new-run2 | 42 | 481,846 | 10,384 |
| new-run3 | 46 | 523,669 | 10,768 |
| old-run1 | 57 | 646,354 | 13,241 |
| old-run2 | 57 | 582,740 | 12,681 |
| old-run3 | 55 | 629,120 | 12,950 |

Matches per file: new 7, 9, 7 (mean 7.7 of 9); old 4, 4, 5 (mean 4.3 of 9). The Q5 and Q7 rules were tightened after a first look at the answers (Q5 requires all 14 class totals, whole numbers accepted; Q7 gives Partial when the answer lists containers beside the roof); both changes are in `score_unattended.py`, and the 2026-10-04 table still reproduces (7, 7, 7 and 5, 6, 4).

## Per-question verdicts for Q7 and Q9

| Question | Run | Verdict | What the agent answered |
|---|---|---|---|
| Q7 | new-run1 | Partial | Named the roof but also listed the project, the building, four storeys and four zones as elements without the set. |
| Q7 | new-run2 | Match | One element, the `IfcRoof` `0jf0rYHfX3RAB3bSIRjmxl`, which has `NRC_OperationalCarbon` but not `NRC_EmbodiedCarbon`. |
| Q7 | new-run3 | Miss | Listed 11 elements (storeys, containers, zones, the project and a roof type definition) and never named the `IfcRoof` element. |
| Q7 | old-run1 | Partial | The `IfcRoof` and the `IfcProject` `0001`; the old file gives the project no embodied set either. |
| Q7 | old-run2 | Partial | The same two elements. |
| Q7 | old-run3 | Match | One element, the `IfcRoof` `0jf0rYHfX3RAB3bSIRjmxl`. |
| Q9 | new-run1 | Match | Unit B Level 1 at 78.04 kWh/m2/yr, read from `NRC_ZoneSummary` through one SQL query over the four zones. |
| Q9 | new-run2 | Match | Unit B Level 1 at 78.04 kWh/m2/yr from `NRC_ZoneSummary`. |
| Q9 | new-run3 | Match | Unit B Level 1 at 78.04 kWh/m2/yr from `NRC_ZoneSummary`, four zone rows sorted. |
| Q9 | old-run1 | Miss | Said the model has no zones (it has none) and offered element-level intensities up to 90.9 instead. |
| Q9 | old-run2 | Miss | Said the model has no zones; zero `IFCZONE` rows. |
| Q9 | old-run3 | Miss | Said the model has no zones; gave the highest element intensity, 90.9 kWh/m2/yr. |

The scorer reads the answer text only; the Q2 and Q7 verdicts should be confirmed against the transcripts (`*.md`), and I read the Q7 and Q9 answers above in them.

## Files

`new-run<n>.md` and `old-run<n>.md` are the transcripts, `.json` the results files the scorer reads, `.log` the progress output of each run, `scores.md` the table and totals.
