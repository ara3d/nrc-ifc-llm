# 6. Proof of concept and results

The proof of concept has two case studies on the same public model. Case study A is the
statement of work's acceptance criterion: natural-language questions answered against an IFC
model enriched with analytics. Case study B applies the same storage and query machinery to
code compliance, and is the study that has been executed and recorded. Both are on the
buildingSMART Duplex Apartment model, `duplex.ifc`, 38,898 STEP entities.

> **Status.** Case study B (6.3) was executed on 2026-08-04 and independently re-run on
> 2026-08-05. Every claim in it is backed by a test or a commit pinned in
> [door-clearance-demo.md](../door-clearance-demo.md). Case study A (6.2) was executed on
> 2026-09-17 with synthetic analytics; its scripts, data, and transcript are in
> [poc/](../poc/README.md), and what it did not cover is listed in the
> [gap report](poc-gap-report.md).

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

**Executed 2026-09-17.** The analytics are synthetic (Section 7.1): each physical element
received a type-based embodied carbon value with a deterministic jitter, and the test kit's
operational carbon and energy intensity columns were reused. The roof deliberately received no
embodied-carbon set.

**Procedure as run.**

1. A generator script produced Layer 1 values for the 218 physical elements (openings excluded),
   storey and building aggregates, a Layer 2 long-format table, and a provenance set for the
   project, following Appendix A.
2. A small .NET program wrote the values into a copy of the model with the byte-exact writer:
   664 property sets, 2,438 typed property values (`IFCREAL`, `IFCLABEL`, `IFCIDENTIFIER`,
   `IFCTEXT`), on 218 elements, 4 storeys, the building, and the project. The entity diff
   listed exactly the 3,766 added entities, removing them restored the source byte for byte,
   and a second run produced identical bytes.
3. The expected answer to each question was computed from the CSV alone, without the IFC file
   or the server.
4. The enriched model was opened through the IFC MCP server over HTTP. The author, acting as
   the agent, asked each question by choosing tool calls, and a helper script recorded every
   call, its arguments, and its result verbatim before the answer was written.

| Item | Value |
|---|---|
| Source entities | 38,898 |
| Enriched entities | 42,664 |
| Property sets written | 664 |
| Property values written | 2,438 |
| Entities added | 3,766 |
| Diff exact, reversible, deterministic | yes, yes, yes |

**Results.** All eight questions were answered from the file through the read-only SQL tool
over the BOS text views. Seven returned values matched the expectation exactly; Q2 did not,
for a reason the transcript makes visible.

| # | Level | Question | Expected | Returned | Calls |
|---|---|---|---|---|---|
| Q1 | Building | Total operational carbon | 37,196.2 kgCO2e/yr | 37,196.2, from both the building aggregate and the sum of 218 elements | 2 |
| Q2 | Storey | Higher mean energy intensity, Level 1 or 2 | L2, marginally: L1 40.50, L2 40.56 over 103 and 93 elements | **L1**: 41.72 against 40.56, over 93 elements each; disagrees | 2 |
| Q3 | Component | Five highest operational carbon | walls 412.0, 410.8; cabinet 402.0; walls 399.7, 398.6 | same five, same order | 1 |
| Q4 | Component | Operational carbon of door `M_Single-Flush:0762 x 2032mm` | 54.0 (first of four) | all four doors listed, 54.0 for the first; ambiguity stated | 1 |
| Q5 | Category | Operational carbon per class | walls 17,547.4; slabs 5,816.9; furnishing 5,766.3 | same, all 14 classes | 1 |
| Q6 | Provenance | Which run, when | run-2026-09-17-01, 2026-09-17 | same, plus tool, method, dataset URI; 664 sets carry the run id | 2 |
| Q7 | Absence | Embodied carbon of the roof | not available | not available, with the two sets the roof does carry | 1 |
| Q8 | Storey | Embodied carbon per storey | L1 49,451.2; L2 48,696.8; T/FDN 11,761.3; Roof 5,821.0 | same | 1 |

Two observations from the transcript matter more than the matches.

- **Q2 needed a second query and still came out wrong.** The converted model's `ContainedIn`
  relation points at the room (Kitchen, Bedroom 1) for elements inside a room and at the
  storey for the rest. The first query grouped by the direct container and produced a list of
  rooms. The agent said so in the transcript and wrote a second query that walks room to
  storey. That query reaches 93 of the 103 Level 1 elements, because ten stair, railing, and
  member parts are aggregated into assemblies rather than contained. The answer stated the
  caveat, but the conclusion it drew (Level 1 higher) is the opposite of the expectation over
  all elements (Level 2 higher by 0.06). The margin is tiny and the synthetic data makes the
  question artificial, but the lesson is real: a per-storey mean derived by the agent from
  relations is only as complete as the relation walk, and the storey aggregates written in
  Layer 1 (Q8) exist precisely so that the answer does not depend on it.
- **Q4 is ambiguous by name.** Four doors share the family name. The agent returned all four
  with their STEP ids and `GlobalId`s rather than choosing one silently.

The full transcript, including the wrong first attempt at Q2, is in
[poc/results/transcript.md](../poc/results/transcript.md).

**Mechanical replay.** The toolkit's `scripts/demo-ifc-mcp.mjs` replays the session's SQL for
Q1, Q5, Q7, and Q8 over the IFC MCP server's stdio transport, the transport an MCP client
uses, and checks each result against `expected_answers.json`. On 2026-09-18 all four matched;
the transcript is [poc/results/transcript-mcp-replay.md](../poc/results/transcript-mcp-replay.md).
This proves the connection and the tool surface end to end without a language model.

**Unattended run, 2026-09-18.** The same eight questions, verbatim, were put to `gpt-5`
through the toolkit's `bimopenmcp-ifc-ask` runner: one fresh conversation per question, the
IFC MCP server in process, no human in the loop. The system prompt names the file, the views
and their columns, and the rules (every number from a tool result; "not available" is a valid
answer). Totals: 35 tool calls, 221,968 input and 30,144 output tokens, toolkit commit
`66df499`. The transcript with every call is
[poc/results/transcript-unattended.md](../poc/results/transcript-unattended.md); the per-question
record is `results-unattended.json`.

| # | Expected | Returned by gpt-5 | Calls | Match |
|---|---|---|---|---|
| Q1 | 37,196.2 | 37,196.2, from the building's own aggregate | 3 | yes |
| Q2 | L2, marginally: 40.50 against 40.56 | Level 2, 40.499 against 40.557, grouped through `StoreyOfEntity` | 4 | yes, where the hand-driven session did not |
| Q3 | walls 412.0, 410.8; cabinet 402.0; walls 399.7, 398.6 | the building (37,196.2) and the four storeys: the query ranked every entity carrying the property, containers included | 3 | no |
| Q4 | 54.0, first of four | all four doors with STEP ids, 54.0 for #8066, and a question back about which one | 4 | yes |
| Q5 | per analytics category: Wall 22,854.1, Floor 5,593.5, ... | per IFC class: IFCWALLSTANDARDCASE 17,547.4, IFCSLAB 5,816.9, ... over 16 rows that include the building and storey aggregates | 3 | partly: the recorded session's grouping, with container rows not excluded |
| Q6 | run-2026-09-17-01, 2026-09-17 | same, from `Pset_NRCAnalyticsProvenance` | 4 | yes |
| Q7 | not available | 1,838.5 kgCO2e A1-A3 from the roof's `IFCSLAB` member, stating that the `IFCROOF` itself carries none | 11 | no, and informative |
| Q8 | L1 49,451.2; L2 48,696.8; T/FDN 11,761.3; Roof 5,821.0 | exactly double each: 98,902.4; 97,393.6; 23,522.6; 11,642.0 | 3 | no |

Four matched, one partly, three did not, and the three misses share one cause that matters
more for the storage recommendation than for the agent. The Layer 1 aggregates written on the
storey and building entities carry the same property set and property name as the element
values. An agent that sums or ranks "everything with `OperationalCarbon_kgCO2e_per_year`" then
counts the building and the storeys as elements (Q3, Q5) and, when it groups elements by storey
through `StoreyOfEntity`, adds the storey's own aggregate to its elements' sum and doubles every
total (Q8). The hand-driven session avoided this by excluding the container classes in each
query, which is the kind of knowledge a prompt can carry but a file should not need. Appendix
A's recommendation should therefore give the aggregate sets their own names (for example
`Pset_NRCStoreySummary`) or their own property names, so that a sum over the element property
cannot include an aggregate of itself.

Q7 is a different lesson. The generator wrote no set on the `IFCROOF`, but the roof is an
assembly whose `IFCSLAB` member received values, and the agent found them, reported them, and
said which entity carries them. The expected answer "not available" was the author's, and the
agent's answer is the better one; the question should be read as being about the roof
assembly, and the absence test in the question list should use an element with no analysed
descendants.

Q2 is the mirror image of the recorded session: the unattended agent used the storey view
the toolkit gained after that session and got the expected ordering over all elements.

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
