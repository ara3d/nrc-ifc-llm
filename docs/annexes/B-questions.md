# Annex B: The nine questions

This annex gives the nine questions the paper asks of the enriched Duplex model. Each has its expected answer, its unit, the rule that scores a language model's answer (in words), and the question graph that computes the answer. Sources: `samples/nrc/questions.txt` (the questions), `samples/nrc-analyses/nrc-q1-*.json` to `nrc-q9-*.json` (the graphs), and `poc/results/expected_answers.json` (Q1 to Q3, Q6, Q8). The values for Q4, Q5, Q7, and Q9 are those the toolkit's question graphs compute at the coming tag `v0.2`; `poc/results/expected_answers.json` still records them under the older wording. The content is the development clone of the BIM Open Toolkit at commit 6f37755. Every analytics value here is synthetic. The graphs are under `samples/nrc-analyses/` in the toolkit.

The model is `samples/nrc/duplex-enriched.ifc`: the buildingSMART Duplex Apartment with 218 analysed elements and the property sets of Annex A. The scorer is `poc/score_unattended.py`. Numbers match when they agree within 0.1 percent. The verdicts are Match, Partial (the expected numbers are present but so is something wrong, such as storey or building rows counted as elements), Miss (a wrong value, or the expected value absent), and Unanswered (an error or the turn limit).

## Q1

- Question: What is the total operational carbon for the building?
- Expected answer: 37 196.2 kgCO2e/yr.
- Scoring rule: the answer states 37 196.2.
- Graph: `nrc-q1-building-total.json`.

## Q2

- Question: Which storey has the higher mean energy intensity, Level 1 or Level 2?
- Expected answer: Level 2, at 40.56 kWh/m2/yr, against 40.5 for Level 1.
- Scoring rule: the answer names Level 2 as higher and states both means. Naming Level 1 as higher is a Miss.
- Graph: `nrc-q2-storey-eui.json`.

## Q3

- Question: Which five elements have the highest operational carbon?
- Expected answer, in kgCO2e/yr:

| Rank | GlobalId | Name | Value |
|---|---|---|---|
| 1 | 0iEHWY1$XA8eQeeULq4jpl | Basic Wall:Interior - Partition (92mm Stud):190140 | 412.0 |
| 2 | 0jf0rYHfX3RAB3bSIRjmr1 | Basic Wall:Exterior - Brick on Block:185101 | 410.8 |
| 3 | 0iEHWY1$XA8eQeeULq4ien | M_Upper Cabinet-Double Door-Wall:1000mm:1000mm:192610 | 402.0 |
| 4 | 3Y4YRln2r91vflHcHE5IVT | Basic Wall:Interior - Furring (38 mm Stud):217415 | 399.7 |
| 5 | 3Y4YRln2r91vflHcHE5IVS | Basic Wall:Interior - Furring (38 mm Stud):217414 | 398.6 |

- Scoring rule: all five values are stated. If the answer also ranks the building total or a storey row as an element, the verdict is Partial.
- Graph: `nrc-q3-top-elements.json`.

## Q4

- Question: What is the operational carbon of the door with GlobalId 1hOSvn6df7F8_7GcBWlS8Z?
- Expected answer: 54.0 kgCO2e/yr. The earlier wording named the door type `M_Single-Flush:0762 x 2032mm`, which four doors share, each with a different value; a GlobalId names one instance.
- Scoring rule: the answer states 54.0.
- Graph: `nrc-q4-door-instances.json`.

## Q5

- Question: How much operational carbon is stored per IFC class?
- Expected answer: 14 class totals, in kgCO2e/yr, summing to 37 196.2.

| IFC class | Operational carbon |
|---|---|
| IFCWALLSTANDARDCASE | 17 547.4 |
| IFCSLAB | 5 816.9 |
| IFCFURNISHINGELEMENT | 5 766.3 |
| IFCFOOTING | 2 086.9 |
| IFCDOOR | 1 324.7 |
| IFCCOVERING | 985.7 |
| IFCWINDOW | 978.9 |
| IFCBEAM | 771.6 |
| IFCMEMBER | 560.0 |
| IFCWALL | 357.5 |
| IFCSTAIRFLIGHT | 311.5 |
| IFCSTAIR | 272.7 |
| IFCROOF | 251.3 |
| IFCRAILING | 164.8 |

- Scoring rule: the answer states the class totals, with the three largest (17 547.4, 5 816.9, 5 766.3) as the minimum check, and does not list storey or building rows as classes (that is Partial).
- Graph: `nrc-q5-by-category.json`.

## Q6

- Question: Which analysis run produced these values, and when?
- Expected answer: run `run-2026-09-17-01`, computed at 2026-09-17T00:00:00Z, by the source tool `nrc-ifc-llm/poc/generate_synthetic_analytics.py`.
- Scoring rule: the answer states the run identifier and the date 2026-09-17.
- Graph: `nrc-q6-analysis-run.json`.

## Q7

- Question: Which analysed elements carry no embodied-carbon property set?
- Expected answer: exactly one, the IfcRoof with GlobalId 0jf0rYHfX3RAB3bSIRjmxl. It has two other metric rows but no embodied carbon. The correct answer reports the absence and does not give an embodied value for it.
- Scoring rule: the answer names the roof and says it has no embodied-carbon property set. Giving an embodied-carbon number as if it existed is a Miss.
- Graph: `nrc-q7-absence.json`.

## Q8

- Question: What is the total embodied carbon (A1-A3) per storey?
- Expected answer, in kgCO2e: Level 1 49 451.2; Level 2 48 696.8; T/FDN 11 761.3; Roof 5 821.0.
- Scoring rule: all four values are stated. Values twice as large are a Miss: they come from adding a storey's stored summary on top of its elements.
- Graph: `nrc-q8-per-storey.json`.

## Q9

- Question: Which zone has the highest energy use intensity?
- Expected answer: Unit B Level 1, at 78.04 kWh/m2/yr (zone energy divided by zone floor area; the four zones are defined in `samples/nrc/nrc-zones.csv`).
- Scoring rule: the answer names Unit B Level 1 and states 78.04.
- Graph: `nrc-q9-zone-eui.json`.
