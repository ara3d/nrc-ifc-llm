# Door Clearance Compliance Demo — Summary

_2026-08-04 · ara3d-sdk + nrc-ifc-llm · one session, two coordinated agents_

## Goal

Demonstrate the full **code → rule → machine checker** pipeline for BIM code compliance:
take a building-code provision, express it as a machine-readable rule, and execute it
automatically against a real IFC model — producing auditable verdicts that satisfy the NRC
TRL/feasibility validation criteria.

## What was built

**1. Ground truth** (independent agent, nrc-ifc-llm [`3a3e844`](https://github.com/ara3d/nrc-ifc-llm/commit/3a3e844e7ec7b4b4852857e166aa5fc241092886))
- All 14 IfcDoor entities in `duplex.ifc` (38,898 STEP entities) extracted: GlobalId,
  name-encoded dimensions, declared `OverallWidth`/`OverallHeight`, containing storey.
- Name-encoded vs declared widths agree to the millimetre on every door.
- Widths: 2× 1250 mm, 6× 864 mm, 4× 762 mm, 2× 813 mm → predicted 8 pass / 6 fail at 850 mm.

**2. Checker** (second agent, ara3d-sdk [`e5dbb6e`](https://github.com/ara3d/ara3d-sdk/commit/e5dbb6e943212e0f62b6d94571a3d0b16a53402a))
- New `tests/Ara3D.DoorClearance.Tests`: JSON rule file (4 provisions, NBC 2020 3.8.3.12-style
  illustrative citations) + evaluation engine + NUnit suite. Reuses the byte-exact IFC
  read/patch/diff machinery; clearance-zone geometry adapted from the Ara 3D Studio
  `IfcDoorClearance` visualization modifier.

**3. Documentation** (nrc-ifc-llm [`dce7a91`](https://github.com/ara3d/nrc-ifc-llm/commit/dce7a91))
- `door-clearance-demo.md` — full expected-vs-observed write-up with pinned links.
- `bos-validation-evidence.md` — evidence inventory updated; gaps 1–3 and 5 marked closed.

## Rules and results (56 verdicts = 14 doors × 4 rules)

| Rule | Requirement | pass | fail | n/a | inconclusive |
|---|---|---|---|---|---|
| DC-W1 | OverallWidth ≥ 850 mm | 8 | 6 | 0 | 0 |
| DC-W2 | Pset_DoorCommon.ClearWidth ≥ 850 mm | 0 | 0 | 0 | 14 |
| DC-M1 | measured vs declared ± 25 mm | 14 | 0 | 0 | 0 |
| DC-Z1 | maneuvering zone unobstructed (Level 1 only) | 4 | 2 | 8 | 0 |
| **Total** | | **26** | **8** | **8** | **14** |

- DC-W1 matched independent ground truth exactly, door by door.
- All four verdict categories occur for honest reasons: DC-W2 inconclusive because the model
  never authors `ClearWidth` (checker refuses to guess); DC-Z1 not-applicable = Level-2 doors
  outside the applicability filter.
- DC-Z1 found **two genuinely obstructed doors** — real furnishing elements inside the
  maneuvering zone; not staged.

## Validation criteria satisfied

| Criterion | Evidence |
|---|---|
| Real IFC model, counted | duplex.ifc — 38,898 entities, 14 doors, 61 obstacles |
| Machine-readable provisions (property + geometric) | 4 JSON rules: 2 property, 2 geometric |
| Deterministic applicability inputs | entity type + storey containment, independently ground-truthed |
| All four verdict categories | 26 / 8 / 8 / 14 |
| Verdicts vs element identifiers with evidence | GlobalId-keyed verdicts.csv, values + citation per record |
| Human confirmation + override recorded | `Ara3D_Compliance` pset appended, diff-verified, byte-identical restore |
| Repeated execution identical, output hash | SHA-256 `a06a44e4…0070e5`, reproduced in an independent fresh run |
| Dated record | 3 commits, 2026-08-04, all pushed |

Test suite: **7/7 passed**, 4 s, Windows 10.0.26200 / .NET 8.0.28 — run twice (agent + independent verification).

## Honest limitations (documented in the project README)

1. Width rule tests the door **leaf**, not code-defined clear width — a strict reading could
   flip the six 864 mm doors (they pass by only 14 mm).
2. Zone clash uses exact placement transforms but obstacle **placement origins**, not meshes;
   mesh-accurate clash via the existing geometry tools is the upgrade path.
3. Citations are illustrative, not legal code text; IDS mapping is future work.
