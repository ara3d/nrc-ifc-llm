# 6. Proof of concept and results

The proof of concept has two case studies on the same public model. Case study A is the
statement of work's acceptance criterion: natural-language questions answered against an IFC
model enriched with analytics. Case study B applies the same storage and query machinery to
code compliance, and is the study that has been executed and recorded. Both are on the
buildingSMART Duplex Apartment model, `duplex.ifc`, 38,898 STEP entities.

> **Status.** Case study B (6.3) was executed on 2026-08-04 and independently re-run on
> 2026-08-05. Every claim in it is backed by a test or a commit pinned in
> [door-clearance-demo.md](../door-clearance-demo.md). Case study A (6.2) is specified but not
> yet executed. Its result tables are empty on purpose.

## 6.1 Model, data, and toolchain

| Item | Detail |
|---|---|
| Model | `duplex.ifc`, buildingSMART Duplex Apartment, IFC2X3, 38,898 entities, 2 storeys |
| Elements with analytics | 268, keyed by `GlobalId`, in `analytics_dataset_with_levels.csv` |
| Analytics columns | `operational_carbon`, `energy_intensity`, `category`, `Level` |
| Doors | 14 (6 on Level 1, 8 on Level 2) |
| Furnishing elements | 61, treated as potential obstacles |
| Toolchain | BIM Open Toolkit at commit `71790a7`; .NET 8; DuckDB |

The toolchain itself is exercised end to end by automated tests before either case study runs.
The IFC-to-BOS conversion, table listing, paged SQL, read-only enforcement, text views,
export, and a cross-check that the storey count from SQL equals the storey count from the
entity tools are all asserted against the FZK-Haus model, and the server is run as a live
subprocess over stdio. [bos-validation-evidence.md](../bos-validation-evidence.md) lists the
tests and commits.

## 6.2 Case study A: natural-language questions over an enriched model

**Planned procedure.**

1. Write the 268 analytics rows into the model as `Pset_NRCOperationalCarbon` and
   `Pset_NRCEnergyPerformance` property sets using the byte-exact writer (Section 3.5), with a
   run id and scenario name. Verify with an entity diff that only the expected entities were
   added.
2. Write storey-level and building-level aggregates as property sets on the two
   `IFCBUILDINGSTOREY` entities and the `IFCBUILDING` entity.
3. Attach an `IfcDocumentReference` to the project naming the CSV, its checksum, and the join key.
4. Open the enriched model through the IFC MCP server from a chat client and ask a fixed list of
   questions at component and building level. Record the transcript, the tool calls, and the
   answer.
5. Compute the expected answer for each question independently with a DuckDB query over the CSV,
   and compare.

**Question list.**

| # | Level | Question | Expected source |
|---|---|---|---|
| Q1 | Building | What is the total operational carbon for the building? | Sum of column |
| Q2 | Storey | Which storey has the higher energy intensity on average? | Group by `Level` |
| Q3 | Component | Which five elements have the highest operational carbon? | Top 5 |
| Q4 | Component | What is the operational carbon of the door named `M_Single-Flush:0762 x 2032mm`? | Lookup |
| Q5 | Category | How much carbon is in structural elements versus other elements? | Group by `category` |
| Q6 | Provenance | Which analysis run produced these values, and when? | Provenance pset |
| Q7 | Absence | What is the embodied carbon of the roof? | No value written; expect "not available" |

Q7 is included to confirm that the agent reports absence rather than inventing a number.

**Results.** To be recorded. The table will hold, per question, the expected value, the
returned value, the number of tool calls, and whether the transcript showed the derivation.

## 6.3 Case study B: door clearance, from code text to verdicts

**Executed 2026-08-04.** This study shows a building-code provision expressed as a
machine-readable rule, executed by a checker against the model, with verdicts stored per element
and a human override written back into the IFC. Figure 1 shows the three stages and the
plan-view geometry of the zone rule.

![Figure 1. Code to rule to checker: the door-clearance pipeline over duplex.ifc](figures/figure-1-door-clearance-pipeline.svg)

_Figure 1. The three stages of case study B: a code provision, its JSON rule, and the checker's
verdict records, with the plan-view zone test of rule DC-Z1 and the verdict totals._

**Rules.** Four provisions modelled on NBC 2020 accessible-door requirements. The citations are
labelled illustrative in the rule file; they are not legal text.

| Rule | Kind | Requirement |
|---|---|---|
| DC-W1 | property threshold | `OverallWidth` at least 850 mm |
| DC-W2 | property threshold | `Pset_DoorCommon.ClearWidth` at least 850 mm |
| DC-M1 | measured versus declared | Width encoded in the type name agrees with `OverallWidth` within 25 mm |
| DC-Z1 | zone unobstructed | Manoeuvring zone in front of the door, depth equal to door width, free of furnishing elements; applies to storey "Level 1" only |

Each rule in the JSON file has an id, a citation, an applicability filter (entity type and
optional storey), requirement parameters, and a sentence of verdict semantics. Appendix B gives
the schema and one full rule.

**Checker.** A small engine loads the rule file, evaluates every rule against every door, and
emits one record per (door, rule) with the verdict and the evidence that produced it. Output is
sorted by (`GlobalId`, rule id) so that it does not depend on file order.

```csharp
public static IReadOnlyList<VerdictRecord> Evaluate(ModelFacts facts, RuleSet rules)
    => facts.Doors
        .SelectMany(door => rules.Rules.Select(rule => Evaluate(door, rule, facts)))
        .OrderBy(v => v.GlobalId, StringComparer.Ordinal)
        .ThenBy(v => v.RuleId, StringComparer.Ordinal)
        .ToList();
```

A property-threshold rule returns `Inconclusive` when the property is absent; it does not
guess. The zone rule composes the door's full placement chain (rotation included) to build an
axis-aligned zone box and tests each furnishing element's placement origin against it.

**Ground truth.** Before the checker was written, a separate agent in a separate commit
extracted every door's STEP id, `GlobalId`, name-encoded width and height (Revit family names
such as `M_Single-Flush:0762 x 2032mm`), declared `OverallWidth` and `OverallHeight`, and
containing storey. Findings: all 14 doors carry both attributes; name-encoded and declared
dimensions agree to the millimetre on every door; widths are 2 at 1250 mm, 6 at 864 mm, 4 at
762 mm, 2 at 813 mm. The ground truth therefore predicted, for DC-W1, 8 pass and 6 fail, with
the 864 mm doors passing by 14 mm and the 813 mm doors failing by 37 mm.

**Results.** 56 verdicts, 14 doors by 4 rules.

| Rule | Pass | Fail | Not applicable | Inconclusive |
|---|---|---|---|---|
| DC-W1 width | 8 | 6 | 0 | 0 |
| DC-W2 clear width pset | 0 | 0 | 0 | 14 |
| DC-M1 measured vs declared | 14 | 0 | 0 | 0 |
| DC-Z1 zone (Level 1 only) | 4 | 2 | 8 | 0 |
| Total | 26 | 8 | 8 | 14 |

- DC-W1 matches ground truth exactly, door by door.
- All four verdict categories occur, each for a real reason. DC-W2 is inconclusive on every
  door because the model's authors never wrote `Pset_DoorCommon.ClearWidth`. DC-Z1's storey
  filter marks the 8 Level 2 doors not applicable.
- DC-Z1 found two Level 1 doors with a furnishing element inside the manoeuvring zone. This
  was not staged; the model contains the condition.
- Every record carries the `GlobalId`, the rule id, the citation, and the evidence values: the
  widths read, the zone bounds, the obstructing element.

**Determinism.** The evaluation runs twice from scratch in the test suite and the SHA-256 of the
verdict CSV is asserted identical. An independent re-run in a fresh process the next day gave
the same hash. Timestamps are kept in a separate run log, never in the hashed output.

**Override.** A failing 762 mm door receives an `Ara3D_Compliance` property set with
`Verdict`, `OverrideVerdict`, `OverrideReason`, and `ReviewedBy`, appended to a copy of the
model with the byte-exact writer. The test asserts three things: the entity diff lists exactly
the added entities and nothing else; removing them restores the source file byte for byte; and
the source model is never modified.

```csharp
File.WriteAllBytes(overriddenPath, IfcPatcher.Append(original, builder.Lines));

using var overridden = IfcSourceFile.Load(overriddenPath);
var diff = IfcDiff.Compare(original, overridden);
Assert.That(diff.Added, Is.EqualTo(builder.Ids));
Assert.That(diff.Deleted, Is.Empty);
Assert.That(diff.Changed, Is.Empty);

var restored = IfcPatcher.Remove(overridden, diff.Added);
Assert.That(restored, Is.EqualTo(File.ReadAllBytes(TestPaths.DuplexIfc)));
```

**Test run.** Seven tests, all passing, in about four seconds on Windows 11 and .NET 8.0.28,
verified twice: once by the implementing agent and once in a fresh session.

## 6.4 What the two studies show together

Case study B exercises every part of the recommended architecture except the language model:
values read from the file, a rule expressed as data, verdicts keyed by `GlobalId` with evidence,
results written back byte-exactly, and reproducibility proven by hash. Case study A adds the
language model in front of the same tools. The studies are deliberately built on one model, one
writer, and one table shape, so that a verdict and a carbon value are the same kind of thing:
a row keyed by `GlobalId` that can be coloured, summed, asked about, and written back.
