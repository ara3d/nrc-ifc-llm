# Appendix B. Rule file schema

The machine-readable provision file used in case study B. It is JSON with one object per rule.
The full file is at
[door-clearance-rules.json](https://github.com/ara3d/bim-open-toolkit/blob/71790a7/tests/Ara3D.DoorClearance.Tests/rules/door-clearance-rules.json).

## Structure

```text
RuleSet
  description        string   Note on provenance; states that citations are illustrative
  rules[]            Rule

Rule
  id                 string   Stable identifier, e.g. "DC-W1"
  citation
    code             string   Code name, e.g. "NBC 2020"
    clause           string   Clause reference
    text             string   Paraphrase of the requirement
  applicability
    entityType       string   IFC entity type the rule applies to
    storey           string?  Storey name filter, or null for all storeys
  requirement
    kind             enum     "property-threshold" | "measured-vs-declared" | "zone-unobstructed"
    source           string   Where the value comes from (attribute, pset, or geometry)
    minWidthMm       number?  For property-threshold
    toleranceMm      number?  For measured-vs-declared
    zoneDepthFactor  number?  For zone-unobstructed: zone depth as a multiple of door width
  verdictSemantics   string   Sentence stating when each verdict is produced
```

The `applicability` object is the same shape as an IDS applicability facet (entity type plus a
container filter), which is what makes the IDS mapping in Section 8.2 straightforward for the
property-threshold kind.

## One rule in full

```json
{
  "id": "DC-Z1",
  "citation": {
    "code": "NBC 2020",
    "clause": "3.8.3.12(3) (illustrative, not legal text)",
    "text": "A clear and level area shall be provided on the latch side and in front of an accessible door, unobstructed by fixed furnishings, sufficient for a wheelchair to approach and operate the door."
  },
  "applicability": { "entityType": "IFCDOOR", "storey": "Level 1" },
  "requirement": {
    "kind": "zone-unobstructed",
    "source": "placement-chain AABB vs IFCFURNISHINGELEMENT placements",
    "zoneDepthFactor": 1.0
  },
  "verdictSemantics": "pass when no furnishing element origin falls inside the clearance zone box (door footprint expanded by one door width); fail when one does; not_applicable outside the storey filter; inconclusive when the door placement cannot be resolved."
}
```

## Verdict record

Each (element, rule) evaluation produces one record. The CSV written by the checker has these
columns, and its SHA-256 is the determinism check.

| Column | Content |
|---|---|
| `GlobalId` | The element |
| `RuleId` | The rule |
| `Verdict` | `Pass`, `Fail`, `NotApplicable`, or `Inconclusive` |
| `Evidence` | The values read and compared, in words |
| `Citation` | Code and clause from the rule |

An example evidence string for DC-W1 on a failing door:

```text
IFCDOOR.OverallWidth attribute = 762 mm; required >= 850 mm
```

## Relation to the dataflow verdict table

The compliance node pack in the toolkit uses the verdict set `Pass`, `Fail`, `NeedsReview`,
`InfoNotAvailable` and the columns `verdict`, `checkId`, `checkTitle`, `citation`. The mapping
from the checker's set is: `Inconclusive` to `InfoNotAvailable`, `NotApplicable` to a row
omitted by the applicability filter before the check node, and `NeedsReview` as an addition
for rows that fail but are flagged by a review expression. A future revision should adopt one
vocabulary.
