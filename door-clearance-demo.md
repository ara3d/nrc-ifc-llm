# Door Clearance Demonstration — Code → Rule → Machine Checker

_Executed and verified 2026-08-04. All links pinned to commits._

This document records an integrated end-to-end demonstration: a building-code provision
(accessible door clear width, NBC 2020 3.8.3.12-style, illustrative wording) expressed as a
machine-readable rule file, executed by an automated checker against a real IFC model, producing
all four verdict categories with per-element evidence, a recorded human override, and repeated
execution verified identical by output hash. It closes, in whole or in part, the gaps listed in
[bos-validation-evidence.md §9](bos-validation-evidence.md).

## The pipeline

**Code.** Four provisions modeled on NBC 2020 accessible-design requirements (citations are
labeled illustrative, not legal text):

| Rule | Kind | Requirement |
|---|---|---|
| DC-W1 | property-threshold | Door `OverallWidth` ≥ 850 mm |
| DC-W2 | property-threshold | `Pset_DoorCommon.ClearWidth` ≥ 850 mm |
| DC-M1 | measured-vs-declared | Name-encoded width agrees with declared `OverallWidth` within ±25 mm |
| DC-Z1 | zone-unobstructed | Maneuvering zone in front of the door (depth = door width) free of furnishing elements; applicability limited to storey "Level 1" |

**Rule.** The provisions are encoded in a machine-readable JSON rule file —
[rules/door-clearance-rules.json](https://github.com/ara3d/ara3d-sdk/blob/e5dbb6e943212e0f62b6d94571a3d0b16a53402a/tests/Ara3D.DoorClearance.Tests/rules/door-clearance-rules.json)
— each with id, citation, applicability filter (entity type + storey), requirement parameters,
and verdict semantics.

**Checker.** A NUnit-driven checker engine —
[tests/Ara3D.DoorClearance.Tests](https://github.com/ara3d/ara3d-sdk/tree/e5dbb6e943212e0f62b6d94571a3d0b16a53402a/tests/Ara3D.DoorClearance.Tests)
— loads the rule file, evaluates every door, and emits one verdict record per (door, rule) with
evidence. It reuses the byte-exact IFC read/patch/diff machinery from
[tests/Ara3D.Ifc.Tests](https://github.com/ara3d/ara3d-sdk/tree/e5dbb6e943212e0f62b6d94571a3d0b16a53402a/tests/Ara3D.Ifc.Tests)
(source-linked, not copied). The clearance-zone geometry follows the approach prototyped in the
Ara 3D Studio visualization modifier
[IfcDoorClearance.cs](https://github.com/ara3d/ara3d-sdk/blob/e5dbb6e943212e0f62b6d94571a3d0b16a53402a/examples/Ara3D.Studio.Examples/BIM%20Tools/IfcDoorClearance.cs):
a zone box in front of the door, sized by the door's own width, placed by the door's transform.

## The model and ground truth

- Model: [IFC-Test-Kit/duplex.ifc](https://github.com/ara3d/nrc-ifc-llm/blob/3a3e844e7ec7b4b4852857e166aa5fc241092886/IFC-Test-Kit/duplex.ifc)
  — 38,898 STEP entities, 14 IfcDoor, 61 furnishing elements considered as obstacles.
- Ground truth was extracted **independently of the checker** (separate agent, separate commit,
  earlier timestamp) into
  [door_ground_truth.csv](https://github.com/ara3d/nrc-ifc-llm/blob/3a3e844e7ec7b4b4852857e166aa5fc241092886/IFC-Test-Kit/door_ground_truth.csv)
  with derivation notes in
  [door_ground_truth.md](https://github.com/ara3d/nrc-ifc-llm/blob/3a3e844e7ec7b4b4852857e166aa5fc241092886/IFC-Test-Kit/door_ground_truth.md):
  per door, the STEP id, GlobalId, name-encoded width/height (Revit family names such as
  `M_Single-Flush:0762 x 2032mm`), declared `OverallWidth`/`OverallHeight`, and containing storey.
- Ground-truth findings: all 14 doors carry both Overall attributes; name-encoded dimensions
  match declared attributes to the millimetre on every door (declared values carry float noise,
  e.g. `0.7619999999999989` m = 762 mm); units confirmed metres via `IFCSIUNIT`. Doors split
  6 on Level 1, 8 on Level 2. Widths: 2× 1250 mm, 6× 864 mm, 4× 762 mm, 2× 813 mm.

## Expected versus observed

Ground truth predicted, for the 850 mm width rule: **8 pass, 6 fail, 0 inconclusive**
(864 mm doors pass by only 14 mm; 813 mm glass doors fail by 37 mm — deliberately
discriminating data near the threshold).

Observed, across 56 verdicts (14 doors × 4 rules):

| Rule | pass | fail | not_applicable | inconclusive |
|---|---|---|---|---|
| DC-W1 width ≥ 850 mm | 8 | 6 | 0 | 0 |
| DC-W2 ClearWidth pset | 0 | 0 | 0 | 14 |
| DC-M1 measured vs declared | 14 | 0 | 0 | 0 |
| DC-Z1 zone unobstructed (Level 1 only) | 4 | 2 | 8 | 0 |
| **Total** | **26** | **8** | **8** | **14** |

- **DC-W1 matches ground truth exactly** — 8 pass / 6 fail, door by door.
- **All four verdict categories occur**, each for an honest reason: DC-W2 is inconclusive on
  every door because the Duplex authors never wrote `Pset_DoorCommon.ClearWidth`, and the checker
  refuses to guess; DC-Z1's storey filter marks the 8 Level-2 doors not applicable.
- **DC-Z1 found two genuinely obstructed Level-1 doors** — real furnishing elements inside the
  maneuvering zone. This was not staged; the model simply contains the condition.
- Every verdict record carries the element GlobalId, the rule id, the citation, and the evidence
  values (the widths read, the zone bounds, the obstructing element).

## Determinism, override, and audit trail

- **Repeated execution, identical output**: the full evaluation runs twice from scratch; the
  SHA-256 of `verdicts.csv` is asserted identical across runs:
  `a06a44e41c5d08b78ee8d01048c883dd2951217da6015a0d17dd4a9e2f0070e5`.
  Independently re-run after the fact (fresh process, 2026-08-05 UTC): same hash. Timestamps
  live only in the run log, never in the hashed artifact.
- **Human override, recorded**: a failing 762 mm door receives an `Ara3D_Compliance` property set
  (`Verdict`, `OverrideVerdict`, `OverrideReason`, `ReviewedBy`) appended to a copy of the model;
  a structural diff proves exactly the expected entities (and nothing else) were added; removing
  them restores the file **byte for byte**. The override is an auditable, reversible record
  inside the IFC itself. The source model is never modified.
- **Run log** (`artifacts/Ara3D.DoorClearance.Tests/run-log.txt`): model path, entity and door
  counts, rule list with citations, verdict counts, output hash, OS and .NET runtime versions,
  UTC timestamp.

## Test results

`dotnet test tests/Ara3D.DoorClearance.Tests` — **7/7 passed** (4 s), on
Windows 10.0.26200 / .NET 8.0.28, verified twice: once by the implementing agent, once
independently in a fresh session. Assertions include: 14 doors found; 762 mm doors fail and
1250 mm doors pass DC-W1; all four verdict categories present; GlobalId keys valid and unique;
Level-1 applicability yields 6 applicable / 8 not applicable; double-run hash identity; override
round trip byte-identical.

## Honest limitations

Documented in the project
[README](https://github.com/ara3d/ara3d-sdk/blob/e5dbb6e943212e0f62b6d94571a3d0b16a53402a/tests/Ara3D.DoorClearance.Tests/README.md):

1. **Leaf width, not clear width.** DC-W1 tests `OverallWidth` (the leaf). True NBC clear width
   subtracts frame, stops, and hinge-side projection — under a strict reading the six 864 mm
   doors could flip to fail. DC-W2 is the honest placeholder for that: it demands an authored
   `ClearWidth` and returns inconclusive when absent.
2. **Placement-level geometry, not meshes.** The zone clash composes the full
   `IFCLOCALPLACEMENT` → `IFCAXIS2PLACEMENT3D` transform chains exactly (rotation included) but
   tests furnishing placement origins against an axis-aligned zone box, rather than meshing
   every obstacle. The mesh-accurate variant is the natural upgrade via the existing
   `ifc_volume` / `ifc_bounds` geometry tools (needs the native web-ifc library).
3. **Citations are illustrative.** The rule file's NBC references convey the shape of a real
   provision; they are not reproductions of code text.

## Commits

| Date | Repo | Commit | Subject |
|---|---|---|---|
| 2026-08-04 | nrc-ifc-llm | [`3a3e844`](https://github.com/ara3d/nrc-ifc-llm/commit/3a3e844e7ec7b4b4852857e166aa5fc241092886) | feat: door ground-truth dataset for clearance compliance demo |
| 2026-08-04 | ara3d-sdk | [`e5dbb6e`](https://github.com/ara3d/ara3d-sdk/commit/e5dbb6e943212e0f62b6d94571a3d0b16a53402a) | feat(door-clearance): code-to-rule-to-checker demo over duplex.ifc |
| 2026-08-04 | nrc-ifc-llm | [`4687fdb`](https://github.com/ara3d/nrc-ifc-llm/commit/4687fdb1f4310726084449cb9633acb1505af038) | docs: inventory existing BOS validation evidence with pinned links |

## Validation checklist coverage

| Criterion | Status |
|---|---|
| One real IFC model, element count stated | ✅ duplex.ifc, 38,898 entities, 14 doors |
| Machine-readable provisions, ≥1 property + ≥1 geometric rule | ✅ 4 rules: 2 property, 2 geometric |
| Deterministic applicability inputs | ✅ entity type + storey containment, ground-truthed independently |
| All four verdict categories produced | ✅ 26 / 8 / 8 / 14 across 56 verdicts |
| Verdicts recorded against element identifiers with evidence | ✅ GlobalId-keyed CSV with values and citations |
| Human confirmation and override recorded | ✅ Ara3D_Compliance pset, diff-verified, byte-reversible |
| Repeated execution identical, verified by output hash | ✅ SHA-256 match across independent runs |
| Expected vs observed, environment, dated commits | ✅ this document + run-log.txt + commit table above |
