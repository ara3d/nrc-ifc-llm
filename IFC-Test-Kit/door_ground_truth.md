# Door ground truth — duplex.ifc

Ground-truth dataset for the door-clearance code-compliance demo (clear-width >= 850 mm rule).
Companion file: `door_ground_truth.csv`.

## Derivation

- Parsed `duplex.ifc` (STEP text) directly; found **14 `IFCDOOR`** entities.
- **StepId / GlobalId / Name** taken verbatim from each entity (GlobalId = attribute 1, Name = attribute 3).
- **NameWidthMm / NameHeightMm** parsed from the Revit family name embedded in Name,
  e.g. `M_Single-Flush:0762 x 2032mm:...` -> 762 x 2032. Two naming variants occur:
  `0762 x 2032mm` (mm suffix on height only) and `1250mm x 2010mm` (mm on both).
- **OverallWidthMm / OverallHeightMm** from the last two IFCDOOR attributes
  (IFC2x3 order: OverallHeight, then OverallWidth).
- **Storey** resolved via `IFCRELCONTAINEDINSPATIALSTRUCTURE` -> `IFCBUILDINGSTOREY` Name.

## Unit handling

`IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.)` — the project length unit is **metres, no prefix**.
OverallHeight/OverallWidth values like `1.25` and `2.032` are therefore metres and were
converted to mm (x1000, rounded to nearest integer) for the CSV. Example: `0.7619999999999989`
-> 762 mm, matching the name-encoded width exactly.

## Data quality

- **No missing data**: every door has OverallWidth, OverallHeight, a parseable name, and a storey.
- **No name/attribute disagreements**: name-encoded dimensions match the Overall attributes
  to the millimetre for all 14 doors (attribute values carry float noise, e.g.
  `2.009999999999999` m = 2010 mm).
- Storey containment: 6 doors on Level 1, 8 on Level 2.

## Expected verdict distribution (clear width >= 850 mm)

| Verdict | Count | Widths |
|---|---|---|
| pass | 8 | 2 x 1250 mm, 6 x 864 mm |
| fail | 6 | 4 x 762 mm, 2 x 813 mm |
| inconclusive | 0 | — |

Note: 864 mm doors pass by only 14 mm and 813 mm doors fail by 37 mm — useful near-threshold
cases for the demo. (Verdicts use OverallWidth as a proxy for clear width; a stricter reading
of clear opening width would subtract frame/leaf allowances and could flip the 864 mm doors.)
